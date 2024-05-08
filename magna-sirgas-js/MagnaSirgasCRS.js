class MagnaSirgasCRS {

    constructor() {
        if (this.constructor === MagnaSirgasCRS) {
            throw new Error("You can't instantiate an abstract class");
        }
    }

    type() {
        return 'MagnaSirgasCRS';
    }

    crs() {
        throw new Error("Abstract method 'crs' must be implemented.");
    }

    maxNorth() {
        throw new Error("Abstract method 'max_north' must be implemented.");
    }

    minSouth() {
        throw new Error("Abstract method 'min_south' must be implemented.");
    }

    maxEast() {
        throw new Error("Abstract method 'max_east' must be implemented.");
    }

    minWest() {
        throw new Error("Abstract method 'min_west' must be implemented.");
    };

    hashObject() {
        throw new Error("Abstract method 'min_west' must be implemented.");
    }

};

module.exports = MagnaSirgasCRS;
