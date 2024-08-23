{pkgs}: {
  deps = [
    pkgs.geckodriver
    pkgs.xvfb-run
    pkgs.chromium
    pkgs.chromedriver
  ];
}
