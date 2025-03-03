/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";
import { isBinarySize } from "@web/core/utils/binary";
import { fileTypeMagicWordMap, imageCacheKey } from "@web/views/fields/image/image_field";
import { CustomSignatureDialog } from "./custom_signature_dialog";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState } from "@odoo/owl";


const placeholder = "/web/static/img/placeholder.png";

export class CustomSignatureField extends Component {
    static template = "web.CustomSignatureField";
    static props = {
        ...standardFieldProps,
        defaultFont: { type: String },
        height: { type: Number, optional: true },
        previewImage: { type: String, optional: true },
        width: { type: Number, optional: true },
    };

    setup() {
    this.notification = useService("notification");
    this.displaySignatureRatio = 3;
    this.dialogService = useService("dialog");
    this.state = useState({
        isValid: true,
        nif: "",
    });
}


    get rawCacheKey() {
        return this.props.record.data.write_date;
    }

    get getUrl() {
    if (!this.value) {
        console.warn("No signature value found, using placeholder.");
        return "/web/static/img/placeholder.png";  // Imagen por defecto
    }

    if (this.value.startsWith("iVBOR")) {  // Si la imagen ya está en base64
        console.log("Using base64 image:", this.value);
        return "data:image/png;base64," + this.value;
    }

    console.log("Generating Odoo image URL...");
    return url("/web/image", {
        model: this.props.record.resModel,
        id: this.props.record.resId,
        field: this.props.name,
        unique: imageCacheKey(this.rawCacheKey),
    });
}


    get sizeStyle() {
        let { width, height } = this.props;

        if (!this.value) {
            if (width && height) {
                width = Math.min(width, this.displaySignatureRatio * height);
                height = width / this.displaySignatureRatio;
            } else if (width) {
                height = width / this.displaySignatureRatio;
            } else if (height) {
                width = height * this.displaySignatureRatio;
            }
        }

        let style = "";
        if (width) {
            style += `width:${width}px; max-width:${width}px;`;
        }
        if (height) {
            style += `height:${height}px; max-height:${height}px;`;
        }
        return style;
    }

    get value() {
    console.log("Fetching value for custom_signature:", this.props.record.data[this.props.name]);
    return this.props.record.data[this.props.name];
}

    onClickSignature() {
        if (!this.props.readonly) {
            const nameAndSignatureProps = {
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
                uploadSignature: (signature) => this.uploadSignature(signature),
            };
            this.dialogService.add(CustomSignatureDialog, dialogProps);
        }
    }

    onLoadFailed() {
    this.state.isValid = false;
    this.notification.add(_t("Could not display the selected image"), {
        type: "danger",
    });
}

    uploadSignature({ signatureImage, nif }) {
    console.log("Uploading signature with NIF:", nif);
    console.log("Signature Image:", signatureImage);
    this.state.nif = nif;
    this.props.record.update({
        [this.props.name]: signatureImage[1] || false,
        nif: nif  // Guardar el NIF en el nuevo campo
    }).then(() => {
        console.log("Signature and NIF updated successfully");
    }).catch((error) => {
        console.error("Error updating signature and NIF:", error);
    });
}

    onNifChange(event) {
        this.state.nif = event.target.value;
    }
}

export const customSignatureField = {
    component: CustomSignatureField,
    fieldDependencies: [{ name: "write_date", type: "datetime" }],
    supportedOptions: [
        {
            label: _t("Prefill with"),
            name: "full_name",
            type: "field",
            availableTypes: ["char", "many2one"],
            help: _t("The selected field will be used to pre-fill the signature"),
        },
        {
            label: _t("Default font"),
            name: "default_font",
            type: "string",
        },
        {
            label: _t("Size"),
            name: "size",
            type: "selection",
            choices: [
                { label: _t("Small"), value: "[0,90]" },
                { label: _t("Medium"), value: "[0,180]" },
                { label: _t("Large"), value: "[0,270]" },
            ],
        },
        {
            label: _t("Preview image field"),
            name: "preview_image",
            type: "field",
            availableTypes: ["binary"],
        },
    ],
    extractProps: ({ attrs, options }) => ({
        defaultFont: options.default_font || "",
        fullName: options.full_name,
        height: options.size ? options.size[1] || undefined : attrs.height,
        previewImage: options.preview_image,
        width: options.size ? options.size[0] || undefined : attrs.width,
    }),
};

registry.category("fields").add("custom_signature", customSignatureField);
