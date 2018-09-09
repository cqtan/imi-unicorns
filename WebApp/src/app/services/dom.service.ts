// Angular Dependencies
import { Injectable, Injector, ComponentFactoryResolver, EmbeddedViewRef, ApplicationRef } from '@angular/core'; 

/*
 * This Service is responsible for searching for certain html-ids and appending
 * or destroying components into them when requested
 */
@Injectable()
export class DomService {

    private childComponentRef: any;

    constructor(
        private componentFactoryResolver: ComponentFactoryResolver,
        private appRef: ApplicationRef,
        private injector: Injector
    ) { }

    public appendComponentTo(parentId: string, child: any, childConfig?: ChildConfig) {
        // Create a component reference from the component 
        let childComponentRef = this.componentFactoryResolver
            .resolveComponentFactory(child)
            .create(this.injector);

        // Attach the config to the child (inputs and outputs)
        this.attachConfig(childConfig, childComponentRef);

        this.childComponentRef = childComponentRef;
        // Attach component to the appRef so that it's inside the ng component tree
        this.appRef.attachView(childComponentRef.hostView);

        // Get DOM element from component
        let childDomElem = (childComponentRef.hostView as EmbeddedViewRef<any>).rootNodes[0] as HTMLElement;

        // Append DOM element to the body
        document.getElementById(parentId).appendChild(childDomElem);

    }

    public removeComponent() {
        this.appRef.detachView(this.childComponentRef.hostView);
        this.childComponentRef.destroy();
    }


    private attachConfig(config, componentRef) {
        let inputs = config.inputs;
        let outputs = config.outputs;
        for (let key in inputs) {
            componentRef.instance[key] = inputs[key];
        }

        for (let key in outputs) {
            componentRef.instance[key] = outputs[key];
        }
    }
}

interface ChildConfig {
    inputs: Object,
    outputs: Object 
}
