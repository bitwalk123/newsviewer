Name:           newsviewer
Version:        0.0.1
Release:        1%{?dist}
Summary:        ニュースビューアー

License:        MIT
BuildArch:      noarch

Source0: %{name}-%{version}.tar.xz

# 依存パッケージ
Requires:       python3-pyside6
Requires:       python3-beautifulsoup4
Requires:       python3-requests

%description
PySide6を使用した、東証および米国株の銘柄の会社サイトのニュースビューアーです。
ユーザー独自のパーサーを ~/.local/share/newsviewer/parsers に追加可能です。

%prep
%setup -q

%install
# 1. ディレクトリ作成
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/abstract
mkdir -p %{buildroot}%{_libdir}/%{name}/funcs
mkdir -p %{buildroot}%{_libdir}/%{name}/parsers
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/applications

# 2. Pythonソースの配置 (ライブラリディレクトリ)
cp app.py %{buildroot}%{_libdir}/%{name}/
cp abstract/parser.py %{buildroot}%{_libdir}/%{name}/abstract/
cp funcs/*.py %{buildroot}%{_libdir}/%{name}/funcs/
cp parsers/NVDA.py %{buildroot}%{_libdir}/%{name}/parsers/
cp parsers/tse_7203.py %{buildroot}%{_libdir}/%{name}/parsers/

# 3. リソースファイルの配置
cp resources/icons/newsviewer.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp %{name}.desktop %{buildroot}%{_datadir}/applications/

# 4. 起動用実行スクリプトの作成
cat <<EOF > %{buildroot}%{_bindir}/%{name}
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:%{_libdir}/%{name}
exec python3 %{_libdir}/%{name}/app.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/icons/hicolor/scalable/apps/newsviewer.svg
%{_datadir}/applications/%{name}.desktop

%license LICENSE
%doc README.md

%changelog
* Fri Feb 13 2026 Fuhito Suguri <bitwalk123@users.noreply.github.com> - 0.0.1-1
- initial release