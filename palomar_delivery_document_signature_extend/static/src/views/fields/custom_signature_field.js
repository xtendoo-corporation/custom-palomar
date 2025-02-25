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
        const { name, previewImage, record } = this.props;
        if (isBinarySize(this.value)) {
            return url("/web/image", {
                model: record.resModel,
                id: record.resId,
                field: previewImage || name,
                unique: imageCacheKey(this.rawCacheKey),
            });
        } else {
            const magic = fileTypeMagicWordMap[this.value[0]] || "png";
            return placeholder;
        }
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
        this.state.nif = nif;
        return this.props.record.update({ [this.props.name]: signatureImage[1] || false });
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
