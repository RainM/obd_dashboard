var fixtures = {};

fixtures.PLATES = [
    {
	w: 1,
	h: 1,
	x: 0,
	y: 0,
	title: 'AT Temp, C',
	canvas_text: 'data-type="radial-gauge"',
	ws_selector: 'at_temp',
	plate_ctor: function(elem) {
	    var options = {
		series: [70],
		chart: {
		    height: 350,
		    type: 'radialBar',
		},
		plotOptions: {
		    radialBar: {
			hollow: {
			    size: '70%',
			}
		    },
		},
		labels: ['Cricket'],
            };
	    
            var chart = new ApexCharts(elem, options);
            chart.render();
	},
	on_update: function(new_value, plate) {
	    
	}
    },
    {
	w: 1,
	h: 1,
	x: 1,
	y: 0,
	title: 'RPM',
	canvas_text: '',
	ws_selector: 'engine_rpm',
	plate_ctor: function(elem) {
	    data_obj = {data: [12]};	    
	    var config = {
		type: "radialGauge",
		data: {
		    datasets: [
			data_obj
		    ]
		},
		options: {
		    domain: [0, 6000],
		}
	    };
	    g =  new Chart(elem.getContext('2d'), config);
	    return [g, data_obj];
	},
	on_update: function(new_value, plate) {
	    plate[1].data = [new_value];
	    plate[0].update()
	}
    },
    {
	w: 2,
	h: 1,
	x: 2,
	y: 0,
	title: 'speed, kph',
	canvas_text: '',
	ws_selector: 'speed',
	plate_ctor: function(elem) {
	    return new Chart(elem.getContext('2d'), {
		type: 'line',
		data: {
			labels: ["A", "B", "C", "O", "G", "W", "S"],
			datasets: [{
				label: 'Company A',
				data: [12, 19, 3, 17, 6, 3, 7],
				backgroundColor: "rgba(182, 213, 139, 0.5)"
			}, {
				label: 'Company B',
				data: [2, 29, 5, 5, 2, 3, 10],
				backgroundColor: "rgba(182, 133, 139, 1)"
			}]
		}
	    });
	},
	on_update: function(new_value, plate) {

	}
    }
];
