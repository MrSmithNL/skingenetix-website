import Foundation
import Vision
import AppKit

// Aims the "eyes down to smile" band by measuring the actual landmarks. Two hardenings,
// both bought by failures on the first version:
//   * Vision returned `noface` on every 6336x2688 NBP frame. It is trained around a
//     modest input size and an extreme close-up at 6K exceeds it, so each image is
//     downscaled to 1400px wide before detection and the result scaled back.
//   * On one frame it locked onto the COLLEAGUE at the microscope - centre 0.186 across,
//     eyes 53% down - and reported it as the subject. Every face is now printed with its
//     size and centre so the pick can be checked rather than trusted; this project has
//     twice believed an auto-measured box that was wrong.
func measure(_ path: String) {
    guard let img = NSImage(contentsOfFile: path),
          let full = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\((path as NSString).lastPathComponent)\tERR\tload"); return
    }
    let W = CGFloat(full.width), H = CGFloat(full.height)
    let target: CGFloat = 1400
    let s = min(1.0, target / W)
    var cg = full
    if s < 1.0, let ctx = CGContext(data: nil, width: Int(W*s), height: Int(H*s),
                                    bitsPerComponent: 8, bytesPerRow: 0,
                                    space: CGColorSpaceCreateDeviceRGB(),
                                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) {
        ctx.interpolationQuality = .high
        ctx.draw(full, in: CGRect(x: 0, y: 0, width: W*s, height: H*s))
        if let scaled = ctx.makeImage() { cg = scaled }
    }
    let req = VNDetectFaceLandmarksRequest()
    do { try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req]) }
    catch { print("\((path as NSString).lastPathComponent)\tERR\tperform"); return }
    guard let faces = req.results, !faces.isEmpty else {
        print("\((path as NSString).lastPathComponent)\tERR\tnoface"); return
    }
    let sorted = faces.sorted { $0.boundingBox.width * $0.boundingBox.height
                              > $1.boundingBox.width * $1.boundingBox.height }
    var parts: [String] = []
    for (i, f) in sorted.enumerated() {
        func pts(_ r: VNFaceLandmarkRegion2D?) -> [CGPoint] {
            guard let r = r else { return [] }
            return r.normalizedPoints.map { p in
                CGPoint(x: f.boundingBox.minX + p.x * f.boundingBox.width,
                        y: f.boundingBox.minY + p.y * f.boundingBox.height) }
        }
        let lm = f.landmarks
        let eyes = pts(lm?.leftEye) + pts(lm?.rightEye)
        let mouth = pts(lm?.outerLips) + pts(lm?.innerLips)
        guard !eyes.isEmpty, !mouth.isEmpty else { continue }
        let eyeY = (1 - eyes.map { $0.y }.max()!) * H     // top of the eyes, in full-res px
        let mouthY = (1 - mouth.map { $0.y }.min()!) * H  // bottom of the lips
        parts.append(String(format: "f%d area=%.3f cx=%.3f eyeY=%.0f mouthY=%.0f",
                            i, f.boundingBox.width * f.boundingBox.height,
                            f.boundingBox.midX, eyeY, mouthY))
    }
    print("\((path as NSString).lastPathComponent)\t\(Int(W))x\(Int(H))\tfaces=\(sorted.count)\t"
          + parts.joined(separator: " | "))
}
for p in CommandLine.arguments.dropFirst() { measure(p) }
