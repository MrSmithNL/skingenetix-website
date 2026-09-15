// Read printed text out of an image using macOS Vision, one file per argument.
//
// WHY: on 2026-09-15 a pdrn-ritual frame came back with "PDRN NIGHT CREAM JAR" printed on the
// jar - the brief's INTERNAL HANDLE for the product, set in type as if it were artwork. Judging
// how often that happens by eye across 376 tiles is not feasible and not trustworthy; every
// label check on this project that relied on looking at a contact sheet has missed something.
// There is no tesseract here and Vision is built in, so this is the cheapest reliable reader.
//
// Prints:  <path>\t<TEXT ALL ON ONE LINE, UPPERCASED>
// Author: Claude Code, 2026-09-15.
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path)\tERROR_LOAD"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false          // product names are not dictionary words
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([req])
        let obs = req.results ?? []
        let text = obs.compactMap { $0.topCandidates(1).first?.string }
                      .joined(separator: " ")
                      .uppercased()
                      .replacingOccurrences(of: "\n", with: " ")
        print("\(path)\t\(text)")
    } catch {
        print("\(path)\tERROR_OCR")
    }
}
