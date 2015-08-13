atapackageCreateFunction() {
    proj_name=$1

    repo_name=${proj_name// /-}
    repo_name="$(tr [A-Z] [a-z] <<< "$repo_name")"

    mkdir $repo_name
    mkdir ./$repo_name/data ./$repo_name/scripts
    touch ./$repo_name/scripts/process.py ./$repo_name/scripts/requirements.txt
    cp ~/LICENSE ./$repo_name/LICENSE
    cp .gitignore ./$repo_name/.gitignore
    touch ./$repo_name/README.md
    echo "# " $proj_name >> ./$repo_name/README.md

    git_user=$GIT_USER
    
    if [ $2 ]
    then
        git_URL=https://api.github.com/orgs/$2/repos
    else
        git_URL=https://api.github.com/user/repos
    fi

    curl -u $git_user $git_URL -d {"\""name"\"":"\""$repo_name"\""}

    cd $repo_name
    git init
    git add .
    git commit -m "intialized"

    if [ $2 ]
    then
        git remote add origin git@github.com/$2/$repo_name.git
    else
        git remote add origin git@github.com:$git_user/$repo_name.git
    fi
}
alias newDP=datapackageCreateFunction
