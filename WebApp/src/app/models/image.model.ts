export interface iImage {
    path: string;
    ppn: string;
    colors: string[];
    siblings: Sibling[];
    subject: string[];
}

export interface Sibling {
    $oid: string;
}
