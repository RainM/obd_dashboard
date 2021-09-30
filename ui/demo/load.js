var DemoGrid = {
  currentSize: 3,
    buildElements: function($gridContainer, items, ws_callbacks) {
      var item, i;
      for (i = 0; i < items.length; i++) {
	  let item = items[i];
	  $item = $(
              '<li>' +
		  '<div class="inner">' +
		  '<div class="titles">' + item.title + '</div>' +
		  '<div class="controls">' +
		  '<a href="#zoom1" class="resize" data-w="1" data-h="1">1x1</a>' +
		  '<a href="#zoom2" class="resize" data-w="2" data-h="1">2x1</a>' +
		  '<a href="#zoom1" class="resize" data-w="1" data-h="2">1x2</a>' +
		  '<a href="#zoom2" class="resize" data-w="2" data-h="2">2x2</a>' +
		  '</div>' +
		  '<canvas ' + item.canvas_text + '></canvas>' + 
		  '</div>' +
		  '</li>'
	  );
	  $item.attr({
              'data-w': item.w,
              'data-h': item.h,
              'data-x': item.x,
              'data-y': item.y
	  });
	  $gridContainer.append($item);
	  	  
	  let elem = $item[0].getElementsByTagName('canvas')[0];
	  let chart = item.plate_ctor(elem);

	  ws_callbacks[item.ws_selector] = function (message) {
	      item.on_update(message, chart)
	  };
      }
  },
  resize: function(size) {
    if (size) {
      this.currentSize = size;
    }
    $('#grid').gridList('resize', this.currentSize);
  },
  flashItems: function(items) {
    // Hack to flash changed items visually
    for (var i = 0; i < items.length; i++) {
      (function($element) {
        $element.addClass('changed')
        setTimeout(function() {
          $element.removeClass('changed');
        }, 0);
      })(items[i].$element);
    }
  }
};

$(window).resize(function() {
  $('#grid').gridList('reflow');
});

$(function() {
    ws_callbacks = {}
    DemoGrid.buildElements($('#grid'), fixtures.PLATES, ws_callbacks);

    socket = new WebSocket("ws://127.0.0.1:8083");
    socket.onmessage = function(msg) {
	event = JSON.parse(msg.data)
	cb = ws_callbacks[event.event_type]
	cb(event.value)
    }

  $('#grid').gridList({
    lanes: DemoGrid.currentSize,
    widthHeightRatio: 264 / 294,
    heightToFontSizeRatio: 0.25,
    onChange: function(changedItems) {
      DemoGrid.flashItems(changedItems);
    }
  });
  $('#grid li .resize').click(function(e) {
    e.preventDefault();
    var itemElement = $(e.currentTarget).closest('li'),
        itemWidth = $(e.currentTarget).data('w'),
        itemHeight = $(e.currentTarget).data('h');

    $('#grid').gridList('resizeItem', itemElement, {
      w: itemWidth,
      h: itemHeight
    });
  });
});

