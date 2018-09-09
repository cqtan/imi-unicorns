import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <router-outlet></router-outlet>
  `
})

/**
 * Angular root app component
 */
export class AppComponent {
  title = 'app';
}
