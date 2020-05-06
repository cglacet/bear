
install_dir=~/.github/bear/back-references
git_repo=git@github.com:cglacet/uuid-scheme.git

url="https://raw.githubusercontent.com/cglacet/install-scripts/master/osx/git-clone.sh?$(date +%s)"
/bin/bash -c "$(curl -fsSL $url)" bash $install_dir $git_repo

url="https://raw.githubusercontent.com/cglacet/install-scripts/master/osx/install-python.sh?$(date +%s)"
/bin/bash -c "$(curl -fsSL $url)"

echo "Adding back-reference links to your ${red}Bear${nc} notes"
echo "----------------------------------------------"
python $install_dir/insert_backreferences.py