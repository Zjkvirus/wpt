// DO NOT EDIT! This test has been generated by /html/canvas/tools/gentest.py.
// OffscreenCanvas test in a worker:2d.color.space.p3.to.srgb
// Description:test getImageData with srsb and uint8 from display p3 uint8 canvas
// Note:

importScripts("/resources/testharness.js");
importScripts("/html/canvas/resources/canvas-tests.js");

var t = async_test("test getImageData with srsb and uint8 from display p3 uint8 canvas");
var t_pass = t.done.bind(t);
var t_fail = t.step_func(function(reason) {
    throw reason;
});
t.step(function() {

  var canvas = new OffscreenCanvas(100, 50);
  var ctx = canvas.getContext('2d', {colorSpace: "display-p3"});

  var color_style = 'rgb(50, 100, 150)';
  var pixel_expected = [50, 100, 150, 255];
  var epsilon = 2;
  ctx.fillStyle = color_style;
  ctx.fillRect(0, 0, 10, 10);

  var pixel = ctx.getImageData(5, 5, 1, 1, {colorSpace: "srgb", storageFormat: "uint8"}).data;
  _assertSame(pixel.length, pixel_expected.length, "pixel.length", "pixel_expected.length");
  assert_approx_equals(pixel[0], pixel_expected[0], 2);
  assert_approx_equals(pixel[1], pixel_expected[1], 2);
  assert_approx_equals(pixel[2], pixel_expected[2], 2);
  assert_approx_equals(pixel[3], pixel_expected[3], 2);
  t.done();
});
done();
