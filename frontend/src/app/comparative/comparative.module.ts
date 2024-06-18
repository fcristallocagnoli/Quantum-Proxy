import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ComparativeRoutingModule } from './comparative-routing.module';
import { ComparativeComponent } from './comparative.component';
import { ViewComparativeComponent } from './view-comparative.component';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        ComparativeRoutingModule,
        FormsModule
    ],
    declarations: [
        ComparativeComponent,
        ViewComparativeComponent
    ]
})
export class ComparativeModule { }