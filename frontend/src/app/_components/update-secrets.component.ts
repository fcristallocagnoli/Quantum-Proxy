import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

interface PlatformList {
    platform: number;
    apiKeys: any[];
}

@Component({ 
    selector: 'update-secrets',
    templateUrl: 'update-secrets.component.html',
})
export class UpdateSecretsComponent implements OnInit {
    form!: FormGroup;
    submitting = false;
    submitted = false;
    deleting = false;

    platformList: PlatformList[] = [];

    platformMap: Map<string, Map<string, string>> = new Map<string, Map<string, string>>();

    userPlatformMap: any;

    constructor(public modal: NgbActiveModal) {
        this.form = new FormGroup({});
    }

    ngOnInit() {
        let i = 0;
        for (let key in this.userPlatformMap) {
            this.platformList.push({ platform: i, apiKeys: [] });
            this.form.addControl(`plat-${i}`, new FormControl(key, Validators.required));
            let j = 0;
            for (let subkey in this.userPlatformMap[key]) {
                this.platformList[i].apiKeys.push(j);
                this.form.addControl(`plat-${i}_key-${j}`, new FormControl(subkey, Validators.required));
                this.form.addControl(`plat-${i}_value-${j}`, new FormControl(this.userPlatformMap[key][subkey]));
                j++;
            }
            i++;
        }
    }

    get f() { return this.form.controls; }

    onSubmit() {
        for (let i = 0; i < this.platformList.length; i++) {
            let apiKeysList = this.platformList[i].apiKeys;
            let apiKeysMap = new Map<string, string>();
            for (let j = 0; j < apiKeysList.length; j++) {
                apiKeysMap.set(this.f[`plat-${i}_key-${j}`].value, this.f[`plat-${i}_value-${j}`].value);
            }
            this.platformMap.set(this.f[`plat-${i}`].value, apiKeysMap);
        }

        // expresa el resultado en un formato JSON
        let result: { [key: string]: { [key: string]: string } } = {};
        this.platformMap.forEach((value, key) => {
            let obj: { [key: string]: string } = {};
            value.forEach((v, k) => {
                obj[k] = v;
            });
            result[key] = obj;
        });

        this.modal.close(result);
    }

    addKeyPair(plat: number) {
        this.form.addControl(`plat-${plat}_key-${this.platformList[plat].apiKeys.length}`, new FormControl('', Validators.required));
        this.form.addControl(`plat-${plat}_value-${this.platformList[plat].apiKeys.length}`, new FormControl(''));
        this.platformList[plat].apiKeys.push(this.platformList[plat].apiKeys.length);
    }

    removeKeyPair(plat: number) {
        this.form.removeControl(`plat-${plat}_key-${this.platformList[plat].apiKeys.length - 1}`);
        this.form.removeControl(`plat-${plat}_value-${this.platformList[plat].apiKeys.length - 1}`);
        this.platformList[plat].apiKeys.pop();
    }

    addPlatform() {
        this.form.addControl(`plat-${this.platformList.length}`, new FormControl('', Validators.required));
        this.platformList.push({ platform: this.platformList.length, apiKeys: []});
    }

    removePlatform() {
        this.form.removeControl(`plat-${this.platformList.length - 1}`);
        this.platformList.pop();
    }

}