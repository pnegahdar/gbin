export INENV_VERSION=0.4.7
function inenv() {
    inenv_helper $@
    rc=$?
    if [[ $rc == '200' ]]; then
        `cat $(inenv_helper extra_source)`
    fi
}
