const Ellipsoidal = require('./EllipsoidalCRS');
const proj4 = require('proj4');

class IntHayford1924 extends Ellipsoidal {
    constructor() {
        super();
        this._crs = proj4.defs('intl_crs', '+proj=longlat +ellps=WGS84');
        this._proj_name = "intl";
    }

    name_from_prj() {
        return this._proj_name;
    }

    crs() {
        return this._crs;
    }

    max_north() {
        return this._max_north;
    }

    min_south() {
        return this._min_south;
    }

    max_east() {
        return this._max_east;
    }

    min_west() {
        return this._min_west;
    }

    hashCode() {
        const crsString = JSON.stringify(this._crs);
        return crypto.createHash('md5').update(crsString).digest('hex');
    }

    equals(value) {
        return this._crs === value._crs;
    }

    toString() {
        return `IntHayford1924 is ${IntHayford1924._crs_type} coming from PROJ (${IntHayford1924._crs}) with limits in longitude (${this.max_east()}, ${this.min_west()}) and in latitude (${this.max_north()}, ${this.min_south()})`;
    }
}

module.exports = IntHayford1924;