# usage bash create.sh -n

# FLAG OPTIONS
while [[ $# > 1 ]]
do
key="$1"

case $key in
    -n|--name)
    PACKAGE_NAME="$2"
    shift # past argument
    ;;
    # -<single letter flag>|--<full name flag>)
    # <VARIABLE ASSIGNED TO>="$2"
    # shift # past argument
    # ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

# Get package name if it doesnt exist
if [ -z ${PACKAGE_NAME} ]; 
    then printf 'Please enter a package name: '; 
    read -r PACKAGE_NAME;
    if [ -z ${PACKAGE_NAME} ]
    then
        printf 'Please enter a package name at the prompt or with the [-n | --name] flag.';
        printf 'Quitting'
        exit 1
    fi
fi

# get license type -- default cc-by-4.0
OPT_ARRAY=(CC-BY-4 MIT GPL CC-BY-4-SA CC-BY-4-NC CC-BY-4-NC-SA CC-BY-4-ND CC-BY-4-NC-ND CC-BY-3 CC-BY-3-SA CC-BY-3-ND CC-BY-3-NC CC-BY-3-NC-SA CC-BY-3-NC-ND CC0-1)
NORMAL=`printf "\033[m"`
MENU=`printf "\033[36m"` #Blue
NUMBER=`printf "\033[33m"` #yellow
FGRED=`printf "\033[41m"`
RED_TEXT=`printf "\033[31m"`
ENTER_LINE=`printf "\033[33m"`

show_menu(){
    printf "${MENU}*********************************************${NORMAL} \n"
    printf "${MENU}**${NUMBER} 1)${FGRED} CC-BY-4.0 ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 2)${MENU} MIT ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 3)${MENU} Gnu Public License ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 4)${MENU} CC-BY-4.0 Share Alike ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 5)${MENU} CC-BY-4.0 Non-Commercial ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 6)${MENU} CC-BY-4.0 Non-Commercial Share Alike ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 7)${MENU} CC-BY-4.0 Non-Derivative ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 8)${MENU} CC-BY-4.0 Non-Derivative ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 9)${MENU} CC-BY-4.0 Non-Commercial Non-Derivative ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 10)${MENU} CC-BY-3.0 ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 11)${MENU} CC-BY-3.0 Share Alike 3.0 ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 12)${MENU} CC-BY-3.0 Non-Derivative ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 13)${MENU} CC-BY-3.0 Non-Commercial ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 14)${MENU} CC-BY-3.0 Non-Commercial Share Alike ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 15)${MENU} CC-BY-3.0 Non-Commercial Non-Derivative ${NORMAL} \n"
    printf "${MENU}**${NUMBER} 16)${MENU} CC0-1.0 ${NORMAL} \n"
    # printf "{MENU}**${NUMBER} <#>)${MENU} <LIC NAME> ${NORMAL} \n"
    printf "${MENU}*********************************************${NORMAL} \n"
    read -p "${ENTER_LINE}Please type a menu option and enter or enter to select default${NORMAL}: " opt
}

while true; do
    show_menu
    if [ -z "$opt" ]; then
        LIC_TYPE=${OPT_ARRAY[0]};
        break;
    elif [[ $opt < 1 ]]  || [[ $opt > 3 ]]; then
        printf "${RED_TEXT}Try again. Select a ${ENTER_LINE}number ${RED_TEXT}from option menu.${NORMAL} \n";
    else
        LIC_TYPE=${OPT_ARRAY[$opt-1]};
        break;
    fi
done

# # Get Git user name
while true; do
    if [ -z ${GIT_USER} ]; then
        printf 'Please enter GItHub username: ';
        read -r GIT_USER;
    else
        break;
    fi
done

# Get org if applicable
read -p "${ENTER_LINE}Please type a organization (or press enter for no org)${NORMAL}: " GIT_ORG

# Make Package
REPO_NAME=${PACKAGE_NAME// /_}
REPO_NAME="$(tr [A-Z] [a-z] <<< "$REPO_NAME")"

mkdir $REPO_NAME
mkdir ./$REPO_NAME/data ./$REPO_NAME/scripts
touch ./$REPO_NAME/scripts/process.py ./$REPO_NAME/scripts/requirements.txt
cp ./.templ/licenses/$LIC_TYPE.templ ./$REPO_NAME/$LIC_TYPE.txt
cp .gitignore ./$REPO_NAME/.gitignore
cp ./.templ/README.md.templ ./$REPO_NAME/README.md
if [ -z ${GIT_ORG} ]; then
    GIT_URL=https://api.github.com/user/repos; 
else
    GIT_URL=https://api.github.com/orgs/$GIT_ORG/repos;
fi

# echo $GIT_USER
# echo $GIT_URL
# echo $REPO_NAME
curl -u $GIT_USER $GIT_URL -d {"\""name"\"":"\""$REPO_NAME"\""}

sleep 10
cd $REPO_NAME
git init
git add .
git commit -m "intialized"

if [ -z ${GIT_ORG} ]; then
    git remote add origin https://github.com/$GIT_USER/$REPO_NAME.git;
else
    git remote add origin https://github.com/$GIT_ORG/$REPO_NAME.git;
fi

git push origin master