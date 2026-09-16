// Read printed text out of an image AND report where it sits, one observation per line.
//
// WHY THIS EXISTS ALONGSIDE ocr-text.swift: verify-labels.py answers "is this line present?",
// which is enough to flag a frame. It is not enough to JUDGE one. The project rule is that a
// suspect label is opened at native pixels before anything is done about it, and to crop at
// native pixels you need to know where the lettering is. ocr-text.swift deliberately joins all
// observations into one string, which throws the coordinates away, and it is a verified-working
// tool that a label QA gate depends on - so this is a sibling rather than a flag on that one.
//
// Prints:  <path>\t<TEXT>\t<x>\t<y>\t<w>\t<h>\t<confidence>
// with x/y/w/h in PIXELS, origin TOP-LEFT (Vision returns normalised, origin bottom-left).
// Author: Claude Code, 2026-09-16.
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path)\tERROR_LOAD\t0\t0\t0\t0\t0"); continue
    }
    let W = CGFloat(cg.width), H = CGFloat(cg.height)
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([req])
        for o in (req.results ?? []) {
            guard let c = o.topCandidates(1).first else { continue }
            let b = o.boundingBox                       // normalised, origin bottom-left
            let x = b.origin.x * W
            let y = (1.0 - b.origin.y - b.size.height) * H   // flip to top-left
            let w = b.size.width * W
            let h = b.size.height * H
            let t = c.string.uppercased().replacingOccurrences(of: "\t", with: " ")
            print("\(path)\t\(t)\t\(Int(x))\t\(Int(y))\t\(Int(w))\t\(Int(h))\t\(String(format: "%.2f", c.confidence))")
        }
    } catch {
        print("\(path)\tERROR_OCR\t0\t0\t0\t0\t0")
    }
}
