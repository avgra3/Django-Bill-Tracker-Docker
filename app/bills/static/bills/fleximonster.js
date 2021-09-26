function processData(dataset) {
    var result = []
    dataset = JSON.parse(dataset);
    dataset.forEach(item => result.push(item.fields));
    return result;
}
$.ajax({
    url: $("#pivot-table-container").attr("data-url"),
    dataType: 'json',
    success: function(data) {
        new Flexmonster({
            container: "#pivot-table-container",
            componentFolder: "https://cdn.flexmonster.com/",
            width: "100%",
            height: 430,
            toolbar: true,
            report: {
                dataSource: {
                    type: "json",
                    data: processData(data),
                    mapping: {
                        "carrierName": {
                            "caption": "Carrier Name"
                        },
                        "paidDate": {
                            "caption": "Paid Date"
                        },
                        "totalPaid": {
                            "caption": "Shipping Cost",
                            "type": "number"
                        },
                        "unit_price": {
                            "caption": "Unit Price",
                            "type": "number"
                        }
                    }
                },
                "slice": {
                    "rows": [{
                        "uniqueName": "carrierName"
                    }],
                    "columns": [{
                            "uniqueName": "paidDate"
                        },
                        {
                            "uniqueName": "[Measures]"
                        }
                    ],
                    "measures": [{
                            "uniqueName": "totalPaid",
                            "aggregation": "sum"
                        },
                        {
                            "uniqueName": "unit_price",
                            "aggregation": "sum"
                        }
                    ]
                }
            }
        });
        new Flexmonster({
            container: "#pivot-chart-container",
            componentFolder: "https://cdn.flexmonster.com/",
            width: "100%",
            height: 430,
            //toolbar: true,
            report: {
                dataSource: {
                    type: "json",
                    data: processData(data),
                    mapping: {
                        "billID": {
                            "caption": "Bill ID"
                        },
                        "paidDate": {
                            "caption": "Paid Date",
                            "type": "year/month"
                        },
                        "totalPaid": {
                            "caption": "Shipping Cost",
                            "type": "number"
                        }
                    }
                },
                "slice": {
                    "rows": [{
                        "uniqueName": "billID"
                    }],
                    "columns": [{
                        "uniqueName": "[Measures]"
                    }],
                    "measures": [{
                        "uniqueName": "Monthly",
                        "formula": "sum(\"totalPaid\")",
                        "caption": "Price"
                    }]
                },
                "options": {
                    datePattern: "yy-MM",
                    "viewType": "charts",
                    "chart": {
                        "type": "pie"
                    }
                }
            }
        });
    }
});

