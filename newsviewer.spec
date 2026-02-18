Name:           newsviewer
Version:        0.0.3
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
mkdir -p %{buildroot}%{_libdir}/%{name}/modules
mkdir -p %{buildroot}%{_libdir}/%{name}/parsers
mkdir -p %{buildroot}%{_libdir}/%{name}/widgets
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/applications

# 2. Pythonソースの配置 (ライブラリディレクトリ)
cp app.py %{buildroot}%{_libdir}/%{name}/
cp abstract/parser.py %{buildroot}%{_libdir}/%{name}/abstract/
cp funcs/assets.py %{buildroot}%{_libdir}/%{name}/funcs/
cp funcs/conv_locale.py %{buildroot}%{_libdir}/%{name}/funcs/
cp funcs/plugin_loader.py %{buildroot}%{_libdir}/%{name}/funcs/
cp funcs/utils.py %{buildroot}%{_libdir}/%{name}/funcs/
cp modules/fetcher.py %{buildroot}%{_libdir}/%{name}/modules/
cp modules/newsviewer.py %{buildroot}%{_libdir}/%{name}/modules/
cp parsers/NVDA.py %{buildroot}%{_libdir}/%{name}/parsers/
cp parsers/tse_7203.py %{buildroot}%{_libdir}/%{name}/parsers/
cp widgets/buttons.py %{buildroot}%{_libdir}/%{name}/widgets/
cp widgets/combos.py %{buildroot}%{_libdir}/%{name}/widgets/
cp widgets/containers.py %{buildroot}%{_libdir}/%{name}/widgets/
cp widgets/layouts.py %{buildroot}%{_libdir}/%{name}/widgets/
cp widgets/tables.py %{buildroot}%{_libdir}/%{name}/widgets/
cp widgets/toolbars.py %{buildroot}%{_libdir}/%{name}/widgets/

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
* Wed Feb 18 2026 Fuhito Suguri <bitwalk123@users.noreply.github.com> - 0.0.3-1
- update to 0.0.3

* Mon Feb 16 2026 Fuhito Suguri <bitwalk123@users.noreply.github.com> - 0.0.2-1
- update to 0.0.2

* Sat Feb 14 2026 Fuhito Suguri <bitwalk123@users.noreply.github.com> - 0.0.1-2
- add/modity app icon

* Fri Feb 13 2026 Fuhito Suguri <bitwalk123@users.noreply.github.com> - 0.0.1-1
- initial release