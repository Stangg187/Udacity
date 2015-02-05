

LandmineClass = EntityClass.extend({
	lifetime: 100,

	kill: function() {
		// This will remove the Landmine's physics
		// body. Note that we haven't written the
		// Physics Engine yet, so this won't work!
		// 
		// gPhysicsEngine.removeBodyAsObj(this.physBody);
		// this.physBody = null;

		// Tell the Game Engine to destroy me as an
		// entity. We've provided a blank removeEntity
		// method in GameEngineClass that we'll fill
		// in later.
		gGameEngine.removeEntity(this);
	},

	update: function() {
		// Subtract 0.05 from lifetime each update call.
		// Once lifetime reaches 0, call 'this.kill' and
		// return.
		this.lifetime -= 0.05;
		if (this.lifetime <= 0) {
			this.kill();
			return;
		}
	}
});

gGameEngine.factory['Landmine'] = LandmineClass;

