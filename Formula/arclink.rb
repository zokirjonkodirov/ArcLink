class Arclink < Formula
  desc "Export Arc Browser pinned tabs to Markdown"
  homepage "https://github.com/zokirjonkodirov/ArcLink"
  url "https://github.com/zokirjonkodirov/ArcLink/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "ebabdff3607e14661ff68a43a62842c6954bd110c74b2cb80dee4a666ae9e670"
  license "MIT"
  version "1.0.0"

  depends_on "python3"

  def install
    bin.install "src/arclink/__main__.py" => "arclink"
    chmod 0755, bin/"arclink"
  end

  test do
    assert_match "arclink", shell_output("#{bin}/arclink --help")
  end
end
