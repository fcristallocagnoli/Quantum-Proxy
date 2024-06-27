import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { StatusComponent } from '@app/_components/properties.component';
import { NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { CreateJobComponent } from './create-job.component';
import { JobsRoutingModule } from './jobs-routing.module';
import { JobsComponent } from './jobs.component';
import { ViewJobComponent } from './view-job.component';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        NgbTooltipModule,
        JobsRoutingModule,
        StatusComponent
    ],
    declarations: [
        JobsComponent,
        CreateJobComponent,
        ViewJobComponent
    ]
})
export class JobsModule { }