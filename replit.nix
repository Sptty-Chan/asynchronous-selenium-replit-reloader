{pkgs}: {
  deps = [
    pkgs.geckodriver
    pkgs.xvfb-run
    pkgs.python39Full
    pkgs.chromium
    pkgs.chromedriver
  ];
}
