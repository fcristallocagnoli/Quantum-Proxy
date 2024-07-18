import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { WizardRoutingModule } from './wizard-routing.module';
import { WizardComponent } from './wizard.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        WizardRoutingModule
    ],
    declarations: [
        WizardComponent
    ]
})
export class WizardModule { }