/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { NameAndSignature } from "@web/core/signature/name_and_signature";
import { _t } from "@web/core/l10n/translation";

export class CustomSignatureDialog extends Component {
    setup() {
        this.title = _t("Adopt Your Signature");
        this.signature = useState({
            name: this.props.defaultName,
            isSignatureEmpty: true,
        });
        this.state = useState({
            nif: "",
        });
    }

    onClickConfirm() {
    console.log("Confirm button clicked");
    console.log("Signature state:", this.signature);
    console.log("NIF state:", this.state.nif);
    this.props.uploadSignature({
        name: this.signature.name,
        signatureImage: this.signature.getSignatureImage(),
        nif: this.state.nif,
    });
    this.props.close();
}

    onNifChange(event) {
        this.state.nif = event.target.value;
    }

    get nameAndSignatureProps() {
        return {
            ...this.props.nameAndSignatureProps,
            signature: this.signature,
        };
    }
}

CustomSignatureDialog.template = "web.CustomSignatureDialog";
CustomSignatureDialog.components = { Dialog, NameAndSignature };
CustomSignatureDialog.defaultProps = {
    defaultName: "",
};
