/**
 * FACTORY WHICH IS RESPONSIBLE TO HANDLE MAKING COMPONENTS/ SERVICES/ MODULES AND OTHER THINGS
 * KNOWN TO THE APPLICATION
 */
import 'rxjs'
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http'
import { BrowserModule } from '@angular/platform-browser';
import { NouisliderModule } from 'ng2-nouislider';
import { NgxPaginationModule } from 'ngx-pagination'
import { Routes, RouterModule } from '@angular/router';
// Application Components
import { AppComponent } from './app.component';
import { CanvasComponent } from './canvas.component';
import { ClusterRowComponent } from './cluster-row.component';
import { ClusterView } from './cluster-view.component';
import { ImageModalComponent } from './image-modal.component';
import { MapView } from './map-view.component';
import { ModalMenuComponent } from './modal-menu.component';
import { TimeSliderComponent } from './time-slider.component';
//  Application Services
import { BookService } from './services/book.service'
import { CategoryService } from './services/category.service';
import { ColorService } from './services/color.service';
import { DomService } from './services/dom.service';
import { ImageService } from './services/image.service';
import { ModalService } from './services/modal.service';
import { GenreService } from './services/genre.service';
import { MapService } from './services/maps.service';


const appRoutes: Routes = [
  { path: '', redirectTo: '/cluster-view', pathMatch: 'full' },
  { path: 'cluster-view', component: ClusterView },
  { path: 'map-view', component: MapView }
];

@NgModule({
  declarations: [
    AppComponent,
    ClusterView,
    CanvasComponent, ClusterRowComponent,
    ImageModalComponent,
    MapView, ModalMenuComponent,
    TimeSliderComponent,
    ImageModalComponent
  ],
  imports: [
    BrowserModule, HttpModule, HttpClientModule, FormsModule, NouisliderModule, ReactiveFormsModule, NgxPaginationModule, RouterModule.forRoot(appRoutes)
  ],
  providers: [
    BookService,
    CategoryService, ColorService,
    DomService,
    ImageService,
    ModalService,MapService,
    GenreService
  ],
  entryComponents: [
    ClusterRowComponent, ModalMenuComponent, ImageModalComponent, TimeSliderComponent
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
