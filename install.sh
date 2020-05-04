nc='\\033[0m'
red='\\033[0;31m'
blue='\\033[0;34m'


if ! command -v git 2>&1 >/dev/null; then 
    if ! command -v brew 2>&1 >/dev/null; then 
        echo "Installing homebrew (https://brew.sh/)"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        echo "Installing Git"
        brew install git
    fi
fi

if ! command -v python &> /dev/null; then 
    echo "Installing Python"
    brew install python
fi


# TEMP solution : (download, execute, remove) 
function temp_solution(){
    TMP_DIR=$(mktemp -d)
    echo "Retreiving source from Github (https://github.com/cglacet)."
    git clone -q git@github.com:cglacet/bear.git $TMP_DIR
    if [ $? -eq 0 ]; then 
        echo "Running python script: "
        python ${TMP_DIR}/insert_backreferences.py | sed 's/^/    /'
    else
        echo "Failed to retreive code from Github"
    fi
    rm -rf $TMP_DIR
}


# Permanent solution : (install or update in a fixed location, execute) 
INSTALL_DIR=~/.bear_plugin/cglacet/back-references
function permanent_solution(){
    mkdir -p $INSTALL_DIR
    cd $INSTALL_DIR
    if ! [ -d .git ]; then
        echo "That's the first time you run this script."
        echo "Retreiving source from Github (${blue}https://github.com/cglacet/bear${nc})."
        git clone -q git@github.com:cglacet/bear.git . &> /dev/null
    fi
    if ! git diff --quiet remotes/origin/HEAD; then 
        echo "Updating source from Github (${blue}https://github.com/cglacet/bear${nc})."
        git pull origin master &> /dev/null
    fi
    echo "Adding back-reference links to your ${red}Bear${nc} notes"
    echo "----------------------------------------------"
    python insert_backreferences.py
}

permanent_solution