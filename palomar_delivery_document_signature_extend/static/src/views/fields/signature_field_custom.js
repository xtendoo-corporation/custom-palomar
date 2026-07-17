/** @odoo-module */

import { registry } from "@web/core/registry";
import { CustomSignatureDialog } from "./custom_signature_dialog";
import { useService } from "@web/core/utils/hooks";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

import { Component } from "@odoo/owl";

export class SignatureWidgetCustom extends Component {
    static template = "web.SignatureWidgetCustom";
    static props = {
        ...standardWidgetProps,
        fullName: { type: String, optional: true },
        highlight: { type: Boolean, optional: true },
        string: { type: String },
        signatureField: { type: String, optional: true },
    };

    setup() {
        this.dialogService = useService("dialog");
        this.orm = useService("orm");
    }

    onClickSignature() {
        const nameAndSignatureProps = {
            mode: "draw",
            displaySignatureRatio: 3,
            signatureType: "signature",
            noInputName: true,
        };
        const { fullName, record } = this.props;
        let defaultName = "";
        if (fullName) {
            let signName;
            const fullNameData = record.data[fullName];
            if (record.fields[fullName].type === "many2one") {
                signName = fullNameData && fullNameData[1];
            } else {
                signName = fullNameData;
            }
            defaultName = signName === "" ? undefined : signName;
        }

        nameAndSignatureProps.defaultFont = this.props.defaultFont;

        const dialogProps = {
            defaultName,
            nameAndSignatureProps,
            uploadSignature: (data) => this.uploadSignature(data),
        };
        this.dialogService.add(CustomSignatureDialog, dialogProps);
    }

    async uploadSignature({ signatureImage,nif }) {
        const file = signatureImage[1];
        const { model, resModel, resId } = this.props.record;
        console.log("Signature image:", file);
        console.log("Signature image type:", typeof file);
        console.log("Signature image length:", file.length);
        console.log("NIF:", nif);

        await this.env.services.orm.write(resModel, [resId], {
            [this.props.signatureField]: file,
               nif: nif,
        });
        await this.props.record.load();
        model.notify();
    }
}

export const signatureWidgetCustom = {
    component: SignatureWidgetCustom,
    extractProps: ({ attrs }) => {
        const { full_name: fullName, highlight, signature_field, string } = attrs;
        return {
            fullName,
            highlight: !!highlight,
            string,
            signatureField: signature_field || "signature",
        };
    },
};

registry.category("view_widgets").add("signature_custom", signatureWidgetCustom);
