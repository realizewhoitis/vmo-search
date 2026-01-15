import fs from 'fs';

try {
    const data = JSON.parse(fs.readFileSync('src/data/vmos.json', 'utf8'));
    console.log(`Loaded ${data.length} items.`);

    let errors = 0;
    data.forEach((item, index) => {
        if (typeof item.code !== 'string') {
            console.error(`Item ${index} id=${item.id}: code is not a string!`, item.code);
            errors++;
        }
        if (typeof item.searchTerms !== 'string') {
            console.error(`Item ${index} id=${item.id}: searchTerms is not a string!`, item.searchTerms);
            errors++;
        }
        if (typeof item.description !== 'string') {
            console.error(`Item ${index} id=${item.id}: description is not a string!`, item.description);
            errors++;
        }
        if (typeof item.model !== 'string') {
            console.error(`Item ${index} id=${item.id}: model is not a string!`, item.model);
            errors++;
        }
        if (typeof item.makeName !== 'string') {
            console.error(`Item ${index} id=${item.id}: makeName is not a string!`, item.makeName);
            errors++;
        }
    });

    if (errors === 0) {
        console.log("All items have correct types.");
    } else {
        console.log(`Found ${errors} errors.`);
    }

} catch (err) {
    console.error("Failed to read JSON:", err);
}
