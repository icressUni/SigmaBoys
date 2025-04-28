// Type definitions for face-api.js
declare namespace faceapi {
  class SsdMobilenetv1Options {
    constructor(options: { minConfidence: number });
  }

  function detectAllFaces(
    input: HTMLImageElement | HTMLVideoElement | HTMLCanvasElement,
    options?: SsdMobilenetv1Options
  ): Promise<Array<any>>;

  function createCanvasFromMedia(
    media: HTMLImageElement | HTMLVideoElement
  ): HTMLCanvasElement;

  function matchDimensions(
    canvas: HTMLCanvasElement,
    dimensions: HTMLVideoElement | { width: number; height: number }
  ): void;

  const nets: {
    ssdMobilenetv1: {
      loadFromUri(path: string): Promise<void>;
    };
  };
}
