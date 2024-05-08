const MagnaSirgasCRS = require('../MagnaSirgasCRS');

class ProjectedCRS extends MagnaSirgasCRS {
    constructor() {
        super();
    }
    crsType() {
        return 'Projected';
    }

    crs() {
        // Implementation
    }

    maxNorth() {
        // Implementation
    }

    minSouth() {
        // Implementation
    }

    maxEast() {
        // Implementation
    }

    minWest() {
        // Implementation
    }

    hashCode() {
        const crsString = JSON.stringify(this.crs());
        return crypto.createHash('md5').update(crsString).digest('hex');
    }

    equals(value) {
        return this.crs() === value;
    }

}

module.exports = ProjectedCRS;