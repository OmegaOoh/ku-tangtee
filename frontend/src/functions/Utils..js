export function loadImage(imgFile) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (e) => {
            resolve(e.target.result); // Resolve with the Data URL
        };

        reader.onerror = (error) => {
            reject(error); // Reject on error
        };
        reader.readAsDataURL(imgFile); // Read the file as a Data URL
    });
}
