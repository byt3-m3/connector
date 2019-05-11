function getSnmpVersion() {
    return $('#SNMP_VERSION').val()
}

function getUsm() {
    return $('#V3_USM').val()
}

function getAuthProto() {
    return $('#AUTH_PROTO').val()
}

function getPrivProto() {
    return $('#PRIV_PROTO').val()
}

function getTarget() {
    return $('#TARGET').val()
}

function getCommunity() {
    return $('#COMMUNITY').val()
}

function getAuthKey() {
    return $('#AUTH_KEY').val()
}

function getMethod() {
    return $('#METHOD').val()
}

function getPrivKey() {
    return $('#PRIV_KEY').val()
}

function getV3User() {
    return $('#V3_USER').val()
}

function getCommand() {
    return $('#COMMAND').val()
}

function getSSHPassword() {
    return $('#SSH_PASSWORD').val()
}

function getSSHUsername() {
    return $('#SSH_USERNAME').val()
}

function getNodeType() {
    return $('#NODE_TYPE').val()
}

function checkOpts() {
    let version = getSnmpVersion();
    let method = getMethod();


    if (method.includes("ssh_")) {
        $('#LABEL_V3_USM').hide();
        $('#V3_USM').hide();
        $('#LABEL_V3_USER').hide();
        $('#V3_USER').hide();
        $('#LABEL_AUTH_KEY').hide();
        $('#AUTH_KEY').hide();
        $('#LABEL_AUTH_PROTO').hide();
        $('#AUTH_PROTO').hide();
        $('#LABEL_PRIV_KEY').hide();
        $('#PRIV_KEY').hide();
        $('#LABEL_PRIV_PROTO').hide();
        $('#PRIV_PROTO').hide();
        $('#LABEL_COMMUNITY').hide();
        $('#COMMUNITY').hide();
        $('#LABEL_SNMP_VERSION').hide();
        $('#SNMP_VERSION').hide();

        $('#LABEL_COMMAND').show();
        $('#COMMAND').show();
        $('#LABEL_SSH_USERNAME').show();
        $('#SSH_USERNAME').show();
        $('#LABEL_SSH_PASSWORD').show();
        $('#SSH_PASSWORD').show();
        $('#LABEL_NODE_TYPE').show();
        $('#NODE_TYPE').show();
    }

    if (method.includes("snmp_")) {
        $('#LABEL_SNMP_VERSION').show();
        $('#SNMP_VERSION').show();

        $('#LABEL_COMMAND').hide();
        $('#COMMAND').hide();
        $('#LABEL_SSH_USERNAME').hide();
        $('#SSH_USERNAME').hide();
        $('#LABEL_SSH_PASSWORD').hide();
        $('#SSH_PASSWORD').hide();
        $('#LABEL_NODE_TYPE').hide();
        $('#NODE_TYPE').hide();

        if (version === "3") {

            $('#LABEL_V3_USM').show();
            $('#V3_USM').show();
            $('#LABEL_V3_USER').show();
            $('#V3_USER').show();
            $('#LABEL_AUTH_KEY').show();
            $('#AUTH_KEY').show();
            $('#LABEL_AUTH_PROTO').show();
            $('#AUTH_PROTO').show();
            $('#LABEL_PRIV_KEY').show();
            $('#PRIV_KEY').show();
            $('#LABEL_PRIV_PROTO').show();
            $('#PRIV_PROTO').show();

            $('#LABEL_COMMUNITY').hide();
            $('#COMMUNITY').hide()

        }
        if (version === "2c" || version === "1") {

            $('#LABEL_V3_USM').hide();
            $('#V3_USM').hide();
            $('#LABEL_V3_USER').hide();
            $('#V3_USER').hide();
            $('#LABEL_AUTH_KEY').hide();
            $('#AUTH_KEY').hide();
            $('#LABEL_AUTH_PROTO').hide();
            $('#AUTH_PROTO').hide();
            $('#LABEL_PRIV_KEY').hide();
            $('#PRIV_KEY').hide();
            $('#LABEL_PRIV_PROTO').hide();
            $('#PRIV_PROTO').hide();


            $('#LABEL_COMMUNITY').show();
            $('#COMMUNITY').show()
        }
    }


}