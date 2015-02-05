

GameEngineClass = Class.extend({

    entities: [],
    factory: {},
    _deferredKill: [],

    //-----------------------------
    init: function () {},

    //-----------------------------
    setup: function () {

        // Create physics engine
        gPhysicsEngine.create();

        // Add contact listener
        gPhysicsEngine.addContactListener({

            PostSolve: function (bodyA, bodyB, impulse) {
                // TASK #1
                //
                // Call the 'GetUserData' of both 'bodyA'
                // and 'bodyB'. This will return the 'userData'
                // field that we created earlier. Remember,
                // we put a pointer to the actual Entity object
                // inside 'userData' called 'ent', so we should
                // be able to use that entity here.
                //
                // To take advantage of this, we've created an
                // empty 'onTouch' function in each Entity. This
                // will take care of any game logic we want to
                // process when collisions occur. The 'onTouch'
                // function takes as input the other physics
                // body the Entity is colliding with, the point
                // of collision, and any impulse to impart on
                // the Entity due to the collision.
                //
                // For now, just call each Entity's 'onTouch'
                // method with the colliding physics body, a
                // null position, and the 'impulse' parameter
                // supplied to the 'PostSolve' contact listener.
                //
                // Later, we'll see the 'onTouch' method in action,
                // and fill in the 'onTouch' method of an entity
                // to actually perform game logic.
                //
                // YOUR CODE HERE
                var bA = bodyA.GetUserData();
                var bB = bodyB.GetUserData();
                bA.ent.onTouch(bodyB, impulse);
                bB.ent.onTouch(bodyA, impulse);
                
            }
        });

    },

    spawnEntity: function (typename) {
        var ent = new (gGameEngine.factory[typename])();

        gGameEngine.entities.push(ent);

        return ent;
    },

    update: function () {

        // Loop through the entities and call that entity's
        // 'update' method, but only do it if that entity's
        // '_killed' flag is set to true.
        //
        // Otherwise, push that entity onto the '_deferredKill'
        // list defined above.
        for (var i = 0; i < gGameEngine.entities.length; i++) {
            var ent = gGameEngine.entities[i];
            if(!ent._killed) {
                ent.update();
            } else {
                gGameEngine._deferredKill.push(ent);
            }
        }

        // Loop through the '_deferredKill' list and remove each
        // entity in it from the 'entities' list.
        //
        // Once you're done looping through '_deferredKill', set
        // it back to the empty array, indicating all entities
        // in it have been removed from the 'entities' list.
        for (var j = 0; j < gGameEngine._deferredKill.length; j++) {
            gGameEngine.entities.erase(gGameEngine._deferredKill[j]);
        }

        gGameEngine._deferredKill = [];

        // Update physics engine
        gPhysicsEngine.update();
    }

});

gGameEngine = new GameEngineClass();

