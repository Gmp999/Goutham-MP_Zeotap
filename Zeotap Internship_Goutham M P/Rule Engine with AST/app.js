const apiUrl = 'http://127.0.0.1:8000'; // Define the API URL here

async function createRule() {
    const rule = document.getElementById('rule').value;
    if (!rule) {
        alert('Please enter a rule.');
        return;
    }

    const response = await fetch(`${apiUrl}/create_rule/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: rule })
    });

    const result = await response.json();
    document.getElementById('output').textContent = JSON.stringify(result, null, 2);
}

async function combineRules() {
    const response = await fetch(`${apiUrl}/combine_rules/`, {
        method: 'POST'
    });

    const result = await response.json();
    document.getElementById('output').textContent = JSON.stringify(result, null, 2);
}

async function evaluateRule() {
    const data = document.getElementById('data').value;
    try {
        const jsonData = JSON.parse(data);

        const response = await fetch(`${apiUrl}/evaluate_rule/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: jsonData })
        });

        const result = await response.json();
        document.getElementById('output').textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        alert('Invalid JSON data.');
    }
}
