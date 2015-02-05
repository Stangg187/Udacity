////////////////////////////////////////////////////////////////////
//
// QUIZ
// 
// Write the 'bind' function so that we have a proper abstraction
// between the keys that are pressed and the actions we want to
// take.
// 
// Next, rewrite 'onKeyUp' and 'onKeyDown' to take advantage of the
// new 'bindings' and 'actions' dictionaries in kind.
// 
// More detailed instructions are below.
// 
// You can assume that our canvas element has an ID of 'my_canvas'.
//
////////////////////////////////////////////////////////////////////

InputEngineClass = Class.extend({

	// A dictionary mapping ASCII key codes to string values
	// describing the action we want to take when that key is
	// pressed.
	bindings: {},

	// A dictionary mapping actions that might be taken in our
	// game to a boolean value indicating whether that action
	// is currently being performed.
	actions: {},

	mouse: {
		x: 0,
		y: 0
	},

	//-----------------------------
	setup: function () {
		// Example usage of bind, where we're setting up
		// the W, A, S, and D keys in that order.
		gInputEngine.bind(87, 'move-up');
		gInputEngine.bind(65, 'move-left');
		gInputEngine.bind(83, 'move-down');
		gInputEngine.bind(68, 'move-right');

		// Adding the event listeners for the appropriate DOM events.
		document.getElementById('my_canvas').addEventListener('mousemove', gInputEngine.onMouseMove);
		document.getElementById('my_canvas').addEventListener('keydown', gInputEngine.onKeyDown);
		document.getElementById('my_canvas').addEventListener('keyup', gInputEngine.onKeyUp);
	},

	//-----------------------------
	onMouseMove: function (event) {
		gInputEngine.mouse.x = event.clientX;
		gInputEngine.mouse.y = event.clientY;
	},

	//-----------------------------
	onKeyDown: function (event) {
		// TASK #2
		// Grab the keyID property of the event object parameter,
		// then set the equivalent element in the 'actions' object
		// to true.
		// 
		// You'll need to use the bindings object you set in 'bind'
		// in order to do this.
		//
		// YOUR CODE HERE
        var action = gInputEngine.bindings[event.keyID];
        if (action) {
            gInputEngine.actions[action] = true;
        }
	},

	//-----------------------------
	onKeyUp: function (event) {
		// TASK #3
		// Grab the keyID property of the event object parameter,
		// then set the equivalent element in the 'actions' object
		// to false.
		// 
		// You'll need to use the bindings object you set in 'bind'
		// in order to do this.
		//
		// YOUR CODE HERE
        var action = gInputEngine.bindings[event.keyID];
        if (action) {
            gInputEngine.actions[action] = false;
        }
	},

	// TASK #1
	// The bind function takes an ASCII keycode
	// and a string representing the action to
	// take when that key is pressed.
	// 
	// Fill in the bind function so that it
	// sets the element at the 'key'th value
	// of the 'bindings' object to be the
	// provided 'action'.
	bind: function (key, action) {
		// YOUR CODE HERE
		gInputEngine.bindings[key] = action;
	}

});

gInputEngine = new InputEngineClass();

