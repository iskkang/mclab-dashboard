(async () => {
    const response = await fetch('/config.json');
    const config = await response.json();
    const firebaseConfig = {
        apiKey: config.apiKey,
        authDomain: config.authDomain,
        projectId: config.projectId,
        storageBucket: config.storageBucket,
        messagingSenderId: config.messagingSenderId,
        appId: config.appId,
        measurementId: config.measurementId
    };

    // Firebase 초기화
    import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
    import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";

    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);

    function fetchAndPlot(collectionName, elementId, title, yLabel) {
        const collectionRef = collection(db, collectionName);
        getDocs(collectionRef).then((querySnapshot) => {
            const data = querySnapshot.docs.map(doc => doc.data());
            const dates = data.map(d => new Date(d.Date));
            const values = data.map(d => d.Value || d.TEU || d['SCFI Value'] || d['Thousand TEU']);

            const trace = {
                x: dates,
                y: values,
                type: 'scatter'
            };

            const layout = {
                title: title,
                xaxis: { title: 'Date' },
                yaxis: { title: yLabel }
            };

            Plotly.newPlot(elementId, [trace], layout);
        }).catch((error) => {
            console.error("Error getting document:", error);
        });
    }

    fetchAndPlot('global_exports', 'chart1', 'Global Exports (TEU by Week)', 'TEU');
    fetchAndPlot('scfi', 'chart2', 'Shanghai Containerized Freight Index (SCFI)', 'SCFI Value');
    fetchAndPlot('port_comparison', 'chart3', 'Top Port Comparison', 'Thousand TEU');
})();
