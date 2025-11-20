// upload-button.tsx

import React, { useRef, type ChangeEvent } from 'react';
import { Database } from 'lucide-react'
import { upload } from '../storeDocumentSlice';
import { useAppDispatch } from "../../../app/hooks";
// import { upload } from "../storeDocumentSlice";

interface ComponentProps {
  className?: string;
}

const UploadButton: React.FC<ComponentProps> = ({ className }) => {
    const dispatch = useAppDispatch();
    // const [file, setFile] = useState<File | undefined>(undefined);

    const hiddenFileInput = useRef<HTMLInputElement>(null);

    const handleUpload = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (files && files.length > 0) {
            // setFile(files[0]);
            dispatch(upload(files[0]))
        }
    };

    const handleClick = () => {
        hiddenFileInput.current?.click();
    };

    return (
        <div
        className={`upload-button ${className} m-2 bg-transparent dark:text-white cursor-pointer hover:text-blue-500`}
        onClick={handleClick}
        >
            <Database size={22} />
            <input
                type='file'
                ref={hiddenFileInput}
                onChange={handleUpload}
                style={{ display: 'none' }}
            />
        </div>
    );
}
export default UploadButton;