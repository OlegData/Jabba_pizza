const { TextDecoder, TextEncoder } = require("util");

if (typeof global.TextEncoder === "undefined") {
  global.TextEncoder = TextEncoder;
}

if (typeof global.TextDecoder === "undefined") {
  global.TextDecoder = TextDecoder;
}

if (typeof global.BroadcastChannel === "undefined") {
  class BroadcastChannel {
    constructor() {}
    postMessage() {}
    close() {}
    onmessage() {}
  }
  global.BroadcastChannel = BroadcastChannel;
}

try {
  const { ReadableStream, WritableStream, TransformStream } = require("node:stream/web");
  if (typeof global.ReadableStream === "undefined") {
    global.ReadableStream = ReadableStream;
  }
  if (typeof global.WritableStream === "undefined") {
    global.WritableStream = WritableStream;
  }
  if (typeof global.TransformStream === "undefined") {
    global.TransformStream = TransformStream;
  }
} catch (_) {
  // Ignore if not available; tests will surface missing globals.
}
