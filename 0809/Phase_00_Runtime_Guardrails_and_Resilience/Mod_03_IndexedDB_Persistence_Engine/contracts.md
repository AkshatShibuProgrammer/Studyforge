# Contracts: Module 03 — IndexedDB Persistence Engine

## 1. Storage Interfaces

```typescript
interface ImageRecord {
    image_id: string;               // Key path
    part_id: string;                // Indexed field
    title: string;
    data_url: string;               // Base64 PNG
    style_recommended: string;
    expanded_prompt: string;
    created_at: string;
    byte_size: number;
}

interface ImageMetadataEntry {
    image_id: string;
    part_id: string;
    title: string;
    style: string;
    hasBinary: boolean;
}

namespace StudyForge.ImageDB {
    function init(): Promise<IDBDatabase>;
    function saveImage(record: ImageRecord): Promise<boolean>;
    function getImage(imageId: string): Promise<ImageRecord | null>;
    function getImagesByPart(partId: string): Promise<ImageRecord[]>;
    function deleteImage(imageId: string): Promise<boolean>;
    function clearAll(): Promise<boolean>;
}
```
