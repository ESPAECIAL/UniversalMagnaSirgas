const MagnaSirgasCRS = require('../MagnaSirgasCRS');

class Ellipsoidal extends MagnaSirgasCRS {
    constructor() {
        super();
    }

    nameFromPrj() {
        // Implementation
    }

    crs() {
        // Implementation
    }

    maxNorth() {
        return 90.0;
    }

    minSouth () {
        return -90.0;
    }

    maxEast() {
        return 180.0;
    }

    minWest() {
        return -180.0;
    }

    crsType() {
        return 'Ellipsoidal';
    }

    hashCode() {
        const crsString = JSON.stringify(this.crs());
        return crypto.createHash('md5').update(crsString).digest('hex');
    }

    nameFromProj() {
        // Implementation
    }

    equals(value) {
        return this.crs() === value;
    }

    toString() {
        // Implementation
    }

}

module.exports = Ellipsoidal;
