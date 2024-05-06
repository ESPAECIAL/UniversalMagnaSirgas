class MagnaSirgasCRS {

    constructor(type) {
        if (this.constructor === MagnaSirgasCRS) {
            throw new Error("You can't instantiate an abstract class");
        }
        this.type = type;
    }

    crs() {
        throw new Error("Abstract method 'crs' must be implemented.");
    }

    max_north() {
        throw new Error("Abstract method 'max_north' must be implemented.");
    }

    min_south() {
        throw new Error("Abstract method 'min_south' must be implemented.");
    }

    max_east() {
        throw new Error("Abstract method 'max_east' must be implemented.");
    }

    min_west() {
        throw new Error("Abstract method 'min_west' must be implemented.");
    };

    hashObject() {
        throw new Error("Abstract method 'min_west' must be implemented.");
    }

};

module.exports = MagnaSirgasCRS;
