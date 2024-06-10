import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { SystemsRoutingModule } from './systems-routing.module';
import { SystemsComponent } from './systems.component';
import { ViewSystemComponent } from './view-system.component';

@NgModule({
    declarations: [
        SystemsComponent,
        ViewSystemComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        SystemsRoutingModule
    ]
})
export class SystemsModule { }