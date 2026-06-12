using Microsoft.Win32.SafeHandles;
using System.Diagnostics;
using System.Runtime.InteropServices;

var cli = CliArguments.Parse(args);

switch (cli.Command)
{
    case "probe":
        return RunProbe(cli);
    case "bench-winusb":
        return RunWinUsbBench(cli);
    case "bench-msc":
        return RunMscBench(cli);
    case "paths":
        return RunPaths(cli);
    case "help":
    case "--help":
    case "-h":
        PrintUsage();
        return 0;
    default:
        Console.Error.WriteLine($"Unknown command: {cli.Command}");
        PrintUsage();
        return 1;
}

static int RunPaths(CliArguments cli)
{
    var instanceId = cli.GetString("instance", WildDefaults.InstanceId) ?? WildDefaults.InstanceId;
    Console.WriteLine($"Instance: {instanceId}");
    var paths = RegistryProbe.GetCandidatePaths(instanceId).ToList();
    if (paths.Count == 0)
    {
        Console.WriteLine("No candidate device interface path found.");
        return 2;
    }

    foreach (var path in paths)
    {
        Console.WriteLine(path);
    }

    return 0;
}

static int RunProbe(CliArguments cli)
{
    var instanceId = cli.GetString("instance", WildDefaults.InstanceId) ?? WildDefaults.InstanceId;
    var statusRequest = cli.GetByte("status-request", 0x42);
    var osVendorCode = cli.GetByte("os-vendor-code", 0x20);
    var paths = RegistryProbe.GetCandidatePaths(instanceId).ToList();

    Console.WriteLine($"Instance: {instanceId}");
    if (paths.Count == 0)
    {
        Console.WriteLine("No candidate interface path found.");
        Console.WriteLine($"Expected custom interface GUID: {WildDefaults.InterfaceGuid:B}");
        return 2;
    }

    foreach (var path in paths)
    {
        Console.WriteLine($"Trying path: {path}");
        if (!WinUsbSession.TryOpen(path, out var session, out var error))
        {
            Console.WriteLine($"  Open failed: {error}");
            continue;
        }

        using (session)
        {
            Console.WriteLine("  WinUsb_Initialize ok");
            Console.WriteLine($"  Device speed: {DescribeSpeed(session.DeviceSpeed)}");
            Console.WriteLine($"  Interface: class=0x{session.Descriptor.InterfaceClass:X2} sub=0x{session.Descriptor.InterfaceSubClass:X2} proto=0x{session.Descriptor.InterfaceProtocol:X2} endpoints={session.Descriptor.NumEndpoints}");
            foreach (var pipe in session.Pipes)
            {
                Console.WriteLine($"  Pipe[{pipe.Index}]: type={pipe.Info.PipeType} id=0x{pipe.Info.PipeId:X2} mps={pipe.Info.MaximumPacketSize} interval={pipe.Info.Interval}");
            }

            ProbeControlTransfer(session.InterfaceHandle, 0xC0, statusRequest, 0, 0, 64, "GET_STATUS");
            ProbeControlTransfer(session.InterfaceHandle, 0xC0, osVendorCode, 0, 0x0007, 18, "MSFT_STRING");
            ProbeControlTransfer(session.InterfaceHandle, 0xC0, osVendorCode, 0, 0x0004, 40, "MS_OS_10_COMPAT");
            ProbeControlTransfer(session.InterfaceHandle, 0xC0, osVendorCode, 0, 0x0005, 146, "MS_OS_10_EXTPROP");

            if (session.TryGetFirstBulkIn(out var bulkIn))
            {
                Console.WriteLine($"  Bulk IN pipe: 0x{bulkIn.Info.PipeId:X2}");
                session.SetPipeTimeout(bulkIn.Info.PipeId, 250);
                TryVendorCommand(session.InterfaceHandle, 0x40, "START");
                ReadBurst(session.InterfaceHandle, bulkIn.Info.PipeId, reads: 8, bufferBytes: 4096);
                TryVendorCommand(session.InterfaceHandle, 0x41, "STOP");
            }
            else
            {
                Console.WriteLine("  No bulk IN pipe detected.");
            }
        }

        return 0;
    }

    Console.WriteLine($"No openable WinUSB interface was found. If only the generic USB interface is present, install the local driver package or register {WildDefaults.InterfaceGuid:B} and re-enumerate the device.");
    return 4;
}

static int RunWinUsbBench(CliArguments cli)
{
    var instanceId = cli.GetString("instance", WildDefaults.InstanceId) ?? WildDefaults.InstanceId;
    var seconds = cli.GetDouble("seconds", 5);
    var readBytes = cli.GetInt32("read-bytes", 16 * 1024);
    var frameBytes = cli.GetInt32("frame-bytes", WildDefaults.FrameBytes);
    var startRequest = cli.GetByte("start-request", 0x40);
    var stopRequest = cli.GetByte("stop-request", 0x41);
    var statusRequest = cli.GetByte("status-request", 0x42);
    var skipStart = cli.GetFlag("skip-start");
    var timeoutMs = cli.GetUInt32("timeout-ms", 500);

    var paths = RegistryProbe.GetCandidatePaths(instanceId).ToList();
    Console.WriteLine($"Instance: {instanceId}");
    Console.WriteLine($"Benchmark window: {seconds:0.###} s");
    Console.WriteLine($"Read size: {readBytes} bytes");
    Console.WriteLine($"Frame bytes: {frameBytes}");

    foreach (var path in paths)
    {
        Console.WriteLine($"Trying path: {path}");
        if (!WinUsbSession.TryOpen(path, out var session, out var error))
        {
            Console.WriteLine($"  Open failed: {error}");
            continue;
        }

        using (session)
        {
            if (!session.TryGetFirstBulkIn(out var bulkIn))
            {
                Console.WriteLine("  No bulk IN pipe detected.");
                return 6;
            }

            session.SetPipeTimeout(bulkIn.Info.PipeId, timeoutMs);
            Console.WriteLine($"  Device speed: {DescribeSpeed(session.DeviceSpeed)}");
            Console.WriteLine($"  Bulk IN pipe: 0x{bulkIn.Info.PipeId:X2} mps={bulkIn.Info.MaximumPacketSize}");
            ProbeControlTransfer(session.InterfaceHandle, 0xC0, statusRequest, 0, 0, 64, "GET_STATUS");

            var started = false;
            if (!skipStart)
            {
                started = TryVendorCommand(session.InterfaceHandle, startRequest, "START");
            }

            try
            {
                var result = BenchmarkWinUsb(session.InterfaceHandle, bulkIn.Info.PipeId, TimeSpan.FromSeconds(seconds), readBytes, frameBytes);
                Console.WriteLine(result.Format("WinUSB"));
                return result.TotalBytes > 0 ? 0 : 7;
            }
            finally
            {
                if (started)
                {
                    TryVendorCommand(session.InterfaceHandle, stopRequest, "STOP");
                }
            }
        }
    }

    Console.WriteLine("No openable WinUSB interface was found.");
    Console.WriteLine($"Expected custom interface GUID: {WildDefaults.InterfaceGuid:B}");
    return 4;
}

static int RunMscBench(CliArguments cli)
{
    var drivePath = cli.GetString("path", null);
    if (string.IsNullOrWhiteSpace(drivePath))
    {
        Console.WriteLine("Missing --path argument, for example --path \\\\.\\PhysicalDrive3");
        return 2;
    }

    var seconds = cli.GetDouble("seconds", 5);
    var offsetBytes = cli.GetInt64("offset-bytes", WildDefaults.MscOffsetBytes);
    var readBytes = cli.GetInt32("read-bytes", WildDefaults.FrameBytes);
    Console.WriteLine($"Drive path: {drivePath}");
    Console.WriteLine($"Benchmark window: {seconds:0.###} s");
    Console.WriteLine($"Offset: 0x{offsetBytes:X}");
    Console.WriteLine($"Read size: {readBytes} bytes");

    try
    {
        var result = BenchmarkMsc(drivePath, TimeSpan.FromSeconds(seconds), offsetBytes, readBytes);
        Console.WriteLine(result.Format("MSC"));
        return result.TotalBytes > 0 ? 0 : 7;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"MSC benchmark failed: {ex.Message}");
        return 5;
    }
}

static TransferBenchmark BenchmarkWinUsb(IntPtr interfaceHandle, byte pipeId, TimeSpan duration, int readBytes, int frameBytes)
{
    var buffer = new byte[readBytes];
    var stopwatch = Stopwatch.StartNew();
    var totalBytes = 0L;
    var readsOk = 0;
    var readsFailed = 0;
    var timeoutReads = 0;

    while (stopwatch.Elapsed < duration)
    {
        if (!WinUsbNative.WinUsb_ReadPipe(interfaceHandle, pipeId, buffer, (uint)buffer.Length, out var transferred, IntPtr.Zero))
        {
            readsFailed++;
            if (Marshal.GetLastWin32Error() == 121)
            {
                timeoutReads++;
            }
            continue;
        }

        totalBytes += transferred;
        readsOk++;
    }

    stopwatch.Stop();
    return new TransferBenchmark(totalBytes, readsOk, readsFailed, timeoutReads, stopwatch.Elapsed, frameBytes);
}

static TransferBenchmark BenchmarkMsc(string drivePath, TimeSpan duration, long offsetBytes, int readBytes)
{
    using var handle = WinUsbNative.CreateFileW(
        drivePath,
        WinUsbNative.GenericRead,
        FileShare.ReadWrite,
        IntPtr.Zero,
        FileMode.Open,
        WinUsbNative.FileAttributeNormal,
        IntPtr.Zero);

    if (handle.IsInvalid)
    {
        throw new IOException($"CreateFile failed with error {Marshal.GetLastWin32Error()}");
    }

    using var stream = new FileStream(handle, FileAccess.Read);
    var buffer = new byte[readBytes];
    var stopwatch = Stopwatch.StartNew();
    var totalBytes = 0L;
    var readsOk = 0;
    var readsFailed = 0;

    while (stopwatch.Elapsed < duration)
    {
        stream.Position = offsetBytes;
        var read = stream.Read(buffer, 0, buffer.Length);
        if (read <= 0)
        {
            readsFailed++;
            continue;
        }

        totalBytes += read;
        readsOk++;
    }

    stopwatch.Stop();
    return new TransferBenchmark(totalBytes, readsOk, readsFailed, 0, stopwatch.Elapsed, readBytes);
}

static void ProbeControlTransfer(IntPtr winUsb, byte requestType, byte request, ushort value, ushort index, ushort length, string label)
{
    var setup = new WinUsbSetupPacket
    {
        RequestType = requestType,
        Request = request,
        Value = value,
        Index = index,
        Length = length
    };

    var buffer = new byte[length];
    if (!WinUsbNative.WinUsb_ControlTransfer(winUsb, setup, buffer, (uint)buffer.Length, out var transferred, IntPtr.Zero))
    {
        Console.WriteLine($"  {label}: failed err={Marshal.GetLastWin32Error()}");
        return;
    }

    Console.WriteLine($"  {label}: ok transferred={transferred}");
    if (transferred > 0)
    {
        Console.WriteLine($"    {Hex(buffer.AsSpan(0, (int)transferred))}");
    }
}

static bool TryVendorCommand(IntPtr winUsb, byte request, string label)
{
    var setup = new WinUsbSetupPacket
    {
        RequestType = 0x40,
        Request = request,
        Value = 0,
        Index = 0,
        Length = 0
    };

    if (!WinUsbNative.WinUsb_ControlTransfer(winUsb, setup, Array.Empty<byte>(), 0, out _, IntPtr.Zero))
    {
        Console.WriteLine($"  {label} failed err={Marshal.GetLastWin32Error()}");
        return false;
    }

    Console.WriteLine($"  {label} ok");
    return true;
}

static void ReadBurst(IntPtr winUsb, byte pipeId, int reads, int bufferBytes)
{
    var buffer = new byte[bufferBytes];
    for (var i = 0; i < reads; i++)
    {
        if (!WinUsbNative.WinUsb_ReadPipe(winUsb, pipeId, buffer, (uint)buffer.Length, out var transferred, IntPtr.Zero))
        {
            Console.WriteLine($"  Read[{i}] failed err={Marshal.GetLastWin32Error()}");
            continue;
        }

        Console.WriteLine($"  Read[{i}] transferred={transferred}");
        if (transferred > 0)
        {
            Console.WriteLine($"    {Hex(buffer.AsSpan(0, (int)Math.Min(transferred, 64)))}");
        }
    }
}

static string DescribeSpeed(byte speedCode)
{
    return speedCode switch
    {
        1 => "Low",
        2 => "Full",
        3 => "High",
        _ => $"Unknown({speedCode})"
    };
}

static string Hex(ReadOnlySpan<byte> data)
{
    return string.Join(" ", data.ToArray().Select(static b => b.ToString("X2")));
}

static void PrintUsage()
{
    Console.WriteLine("""
WildWinUsbProbe commands:

  probe [--instance <instanceId>]
      Enumerate candidate interface paths, attempt WinUSB open, and dump interface details.

  paths [--instance <instanceId>]
      Print the candidate interface paths gathered from registry and device-interface classes.

  bench-winusb [--instance <instanceId>] [--seconds 5] [--read-bytes 16384]
               [--frame-bytes 163840] [--start-request 0x40] [--stop-request 0x41]
               [--status-request 0x42] [--timeout-ms 500] [--skip-start]
      Benchmark WinUSB bulk-IN throughput and report equivalent frames per second.

  bench-msc --path \\.\PhysicalDriveN [--seconds 5] [--offset-bytes 0x200000] [--read-bytes 163840]
      Benchmark the legacy MSC preview loop by repeatedly reading the fixed camera frame window.
""");
}

internal static class WildDefaults
{
    public const string InstanceId = @"USB\VID_0483&PID_572A\2004BF1A0800";
    public static readonly Guid InterfaceGuid = new("6C303587-B774-4A8B-8AFF-20557620207A");
    public const int FrameBytes = 320 * 512;
    public const long MscOffsetBytes = 0x1000L * 512L;
}

internal sealed class CliArguments
{
    private readonly Dictionary<string, string?> _options;

    private CliArguments(string command, Dictionary<string, string?> options)
    {
        Command = command;
        _options = options;
    }

    public string Command { get; }

    public static CliArguments Parse(string[] args)
    {
        var command = args.Length == 0 ? "probe" : args[0].Trim();
        if (command.StartsWith("--", StringComparison.Ordinal))
        {
            command = "probe";
        }

        var options = new Dictionary<string, string?>(StringComparer.OrdinalIgnoreCase);
        for (var i = command == "probe" && args.Length > 0 && args[0].StartsWith("--", StringComparison.Ordinal) ? 0 : 1; i < args.Length; i++)
        {
            var token = args[i];
            if (!token.StartsWith("--", StringComparison.Ordinal))
            {
                continue;
            }

            var key = token[2..];
            if ((i + 1) < args.Length && !args[i + 1].StartsWith("--", StringComparison.Ordinal))
            {
                options[key] = args[++i];
            }
            else
            {
                options[key] = null;
            }
        }

        return new CliArguments(command, options);
    }

    public string? GetString(string key, string? defaultValue)
    {
        return _options.TryGetValue(key, out var value) && !string.IsNullOrWhiteSpace(value) ? value : defaultValue;
    }

    public bool GetFlag(string key)
    {
        return _options.ContainsKey(key);
    }

    public int GetInt32(string key, int defaultValue)
    {
        return TryParseInt64(key, out var value) ? checked((int)value) : defaultValue;
    }

    public long GetInt64(string key, long defaultValue)
    {
        return TryParseInt64(key, out var value) ? value : defaultValue;
    }

    public uint GetUInt32(string key, uint defaultValue)
    {
        return TryParseInt64(key, out var value) ? checked((uint)value) : defaultValue;
    }

    public double GetDouble(string key, double defaultValue)
    {
        if (_options.TryGetValue(key, out var value) &&
            !string.IsNullOrWhiteSpace(value) &&
            double.TryParse(value, out var parsed))
        {
            return parsed;
        }

        return defaultValue;
    }

    public byte GetByte(string key, byte defaultValue)
    {
        return TryParseInt64(key, out var value) ? checked((byte)value) : defaultValue;
    }

    private bool TryParseInt64(string key, out long value)
    {
        value = 0;
        if (!_options.TryGetValue(key, out var raw) || string.IsNullOrWhiteSpace(raw))
        {
            return false;
        }

        if (raw.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
        {
            return long.TryParse(raw[2..], System.Globalization.NumberStyles.HexNumber, null, out value);
        }

        return long.TryParse(raw, out value);
    }
}

internal readonly record struct TransferBenchmark(
    long TotalBytes,
    int ReadsOk,
    int ReadsFailed,
    int TimeoutReads,
    TimeSpan Elapsed,
    int FrameBytes)
{
    public string Format(string label)
    {
        var seconds = Math.Max(Elapsed.TotalSeconds, 0.000001);
        var mbPerSecond = TotalBytes / seconds / (1024.0 * 1024.0);
        var frameRate = FrameBytes > 0 ? TotalBytes / seconds / FrameBytes : 0;
        return $"{label} result: bytes={TotalBytes} elapsed_s={seconds:0.###} MBps={mbPerSecond:0.###} fps_equiv={frameRate:0.###} reads_ok={ReadsOk} reads_failed={ReadsFailed} timeouts={TimeoutReads}";
    }
}

internal sealed class WinUsbSession : IDisposable
{
    private WinUsbSession(
        string path,
        SafeFileHandle deviceHandle,
        IntPtr interfaceHandle,
        UsbInterfaceDescriptor descriptor,
        IReadOnlyList<PipeInfo> pipes,
        byte deviceSpeed)
    {
        Path = path;
        DeviceHandle = deviceHandle;
        InterfaceHandle = interfaceHandle;
        Descriptor = descriptor;
        Pipes = pipes;
        DeviceSpeed = deviceSpeed;
    }

    public string Path { get; }
    public SafeFileHandle DeviceHandle { get; }
    public IntPtr InterfaceHandle { get; }
    public UsbInterfaceDescriptor Descriptor { get; }
    public IReadOnlyList<PipeInfo> Pipes { get; }
    public byte DeviceSpeed { get; }

    public static bool TryOpen(string path, out WinUsbSession session, out string error)
    {
        session = null!;
        error = string.Empty;

        var handle = WinUsbNative.CreateFileW(
            path,
            WinUsbNative.GenericRead | WinUsbNative.GenericWrite,
            FileShare.Read | FileShare.Write,
            IntPtr.Zero,
            FileMode.Open,
            WinUsbNative.FileAttributeNormal,
            IntPtr.Zero);

        if (handle.IsInvalid)
        {
            error = $"CreateFile failed: {Marshal.GetLastWin32Error()}";
            handle.Dispose();
            return false;
        }

        if (!WinUsbNative.WinUsb_Initialize(handle, out var interfaceHandle))
        {
            error = $"WinUsb_Initialize failed: {Marshal.GetLastWin32Error()}";
            handle.Dispose();
            return false;
        }

        if (!WinUsbNative.WinUsb_QueryInterfaceSettings(interfaceHandle, 0, out var descriptor))
        {
            error = $"WinUsb_QueryInterfaceSettings failed: {Marshal.GetLastWin32Error()}";
            WinUsbNative.WinUsb_Free(interfaceHandle);
            handle.Dispose();
            return false;
        }

        var pipes = new List<PipeInfo>(descriptor.NumEndpoints);
        for (byte i = 0; i < descriptor.NumEndpoints; i++)
        {
            if (WinUsbNative.WinUsb_QueryPipe(interfaceHandle, 0, i, out var pipe))
            {
                pipes.Add(new PipeInfo(i, pipe));
            }
        }

        var speed = (byte)0;
        var speedLength = 1u;
        if (WinUsbNative.WinUsb_QueryDeviceInformation(interfaceHandle, 1, ref speedLength, out speed) == false)
        {
            speed = 0;
        }

        session = new WinUsbSession(path, handle, interfaceHandle, descriptor, pipes, speed);
        return true;
    }

    public bool TryGetFirstBulkIn(out PipeInfo pipe)
    {
        pipe = Pipes.FirstOrDefault(static p => (p.Info.PipeType == UsbdPipeType.Bulk) && ((p.Info.PipeId & 0x80) != 0));
        return pipe.Info.PipeId != 0;
    }

    public void SetPipeTimeout(byte pipeId, uint timeoutMs)
    {
        WinUsbNative.WinUsb_SetPipePolicy(InterfaceHandle, pipeId, 0x03, sizeof(uint), ref timeoutMs);
    }

    public void Dispose()
    {
        if (InterfaceHandle != IntPtr.Zero)
        {
            WinUsbNative.WinUsb_Free(InterfaceHandle);
        }

        DeviceHandle.Dispose();
    }
}

internal readonly record struct PipeInfo(byte Index, WinUsbPipeInformation Info);

internal static class RegistryProbe
{
    private static readonly Guid GuidDevInterfaceUsbDevice = new("A5DCBF10-6530-11D2-901F-00C04FB951ED");
    private static readonly Guid GuidUsb512WinUsb = new("4F6A8C79-3F02-4B0D-9E2C-1A9B5C7D42E1");
    private static readonly Guid GuidCe32LatencyProbe = new("D2A5C7A3-7A7B-4D5A-A0F3-4AEEA41E62C0");

    public static IEnumerable<string> GetCandidatePaths(string instanceId)
    {
        var yielded = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var instanceSuffix = instanceId.Split('\\').LastOrDefault() ?? string.Empty;

        foreach (var path in EnumeratePaths(GuidDevInterfaceUsbDevice))
        {
            if (PathMatchesInstance(path, instanceId) && yielded.Add(path))
            {
                yield return path;
            }
        }

        foreach (var path in EnumeratePaths(GuidUsb512WinUsb))
        {
            if (yielded.Add(path))
            {
                yield return path;
            }
        }

        foreach (var path in EnumeratePaths(GuidCe32LatencyProbe))
        {
            if (yielded.Add(path))
            {
                yield return path;
            }
        }

        foreach (var path in EnumeratePaths(WildDefaults.InterfaceGuid))
        {
            if (yielded.Add(path))
            {
                yield return path;
            }
        }

        using var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey($@"SYSTEM\CurrentControlSet\Enum\USB\VID_0483&PID_572A\{instanceSuffix}\Device Parameters");
        var symbolicName = key?.GetValue("SymbolicName") as string;
        if (!string.IsNullOrWhiteSpace(symbolicName))
        {
            var normalized = symbolicName.Replace(@"\??\", @"\\?\");
            if (yielded.Add(normalized))
            {
                yield return normalized;
            }
        }
    }

    private static bool PathMatchesInstance(string path, string instanceId)
    {
        var normalizedInstance = instanceId.Replace(@"\", "#", StringComparison.OrdinalIgnoreCase);
        return path.Contains(normalizedInstance, StringComparison.OrdinalIgnoreCase);
    }

    private static IEnumerable<string> EnumeratePaths(Guid guid)
    {
        const int crSuccess = 0;
        var classGuid = guid;
        if (CfgMgr32.CM_Get_Device_Interface_List_SizeW(out var charCount, ref classGuid, null, 0) != crSuccess || charCount <= 1)
        {
            yield break;
        }

        var buffer = new char[charCount];
        if (CfgMgr32.CM_Get_Device_Interface_ListW(ref classGuid, null, buffer, buffer.Length, 0) != crSuccess)
        {
            yield break;
        }

        var start = 0;
        while (start < buffer.Length)
        {
            var end = start;
            while ((end < buffer.Length) && (buffer[end] != '\0'))
            {
                end++;
            }

            if (end == start)
            {
                yield break;
            }

            yield return new string(buffer, start, end - start);
            start = end + 1;
        }
    }
}

internal static class CfgMgr32
{
    [DllImport("cfgmgr32.dll", CharSet = CharSet.Unicode)]
    internal static extern int CM_Get_Device_Interface_List_SizeW(
        out int interfaceListLength,
        ref Guid interfaceClassGuid,
        string? deviceId,
        int flags);

    [DllImport("cfgmgr32.dll", CharSet = CharSet.Unicode)]
    internal static extern int CM_Get_Device_Interface_ListW(
        ref Guid interfaceClassGuid,
        string? deviceId,
        char[] buffer,
        int bufferLength,
        int flags);
}

[StructLayout(LayoutKind.Sequential, Pack = 1)]
internal struct WinUsbSetupPacket
{
    public byte RequestType;
    public byte Request;
    public ushort Value;
    public ushort Index;
    public ushort Length;
}

[StructLayout(LayoutKind.Sequential)]
internal struct UsbInterfaceDescriptor
{
    public byte Length;
    public byte DescriptorType;
    public byte InterfaceNumber;
    public byte AlternateSetting;
    public byte NumEndpoints;
    public byte InterfaceClass;
    public byte InterfaceSubClass;
    public byte InterfaceProtocol;
    public byte Interface;
}

[StructLayout(LayoutKind.Sequential)]
internal struct WinUsbPipeInformation
{
    public UsbdPipeType PipeType;
    public byte PipeId;
    public ushort MaximumPacketSize;
    public byte Interval;
}

internal enum UsbdPipeType
{
    Control,
    Isochronous,
    Bulk,
    Interrupt
}

internal static class WinUsbNative
{
    public const uint GenericRead = 0x80000000;
    public const uint GenericWrite = 0x40000000;
    public const uint FileAttributeNormal = 0x00000080;

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    internal static extern SafeFileHandle CreateFileW(
        string fileName,
        uint desiredAccess,
        FileShare shareMode,
        IntPtr securityAttributes,
        FileMode creationDisposition,
        uint flagsAndAttributes,
        IntPtr templateFile);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_Initialize(
        SafeFileHandle deviceHandle,
        out IntPtr interfaceHandle);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_Free(
        IntPtr interfaceHandle);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_QueryInterfaceSettings(
        IntPtr interfaceHandle,
        byte alternateInterfaceNumber,
        out UsbInterfaceDescriptor usbAltInterfaceDescriptor);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_QueryPipe(
        IntPtr interfaceHandle,
        byte alternateInterfaceNumber,
        byte pipeIndex,
        out WinUsbPipeInformation pipeInformation);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_QueryDeviceInformation(
        IntPtr interfaceHandle,
        uint informationType,
        ref uint bufferLength,
        out byte buffer);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_SetPipePolicy(
        IntPtr interfaceHandle,
        byte pipeId,
        uint policyType,
        uint valueLength,
        ref uint value);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_ReadPipe(
        IntPtr interfaceHandle,
        byte pipeId,
        [Out] byte[] buffer,
        uint bufferLength,
        out uint lengthTransferred,
        IntPtr overlapped);

    [DllImport("winusb.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool WinUsb_ControlTransfer(
        IntPtr interfaceHandle,
        WinUsbSetupPacket setupPacket,
        [In, Out] byte[] buffer,
        uint bufferLength,
        out uint lengthTransferred,
        IntPtr overlapped);
}
