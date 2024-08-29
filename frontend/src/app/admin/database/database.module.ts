import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DatabaseComponent } from './database.component';
import { DatabaseRoutingModule } from './database-routing.module';
import { ProvidersAdminComponent } from './providers-admin.component';
import { AddEditProviderComponent } from './add-edit-provider.component';


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        DatabaseRoutingModule
    ],
    declarations: [
        DatabaseComponent,
        ProvidersAdminComponent,
        AddEditProviderComponent
    ]
})
export class DatabaseModule { }