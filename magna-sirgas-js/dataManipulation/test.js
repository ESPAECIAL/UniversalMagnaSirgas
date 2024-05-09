printsFinalMessage() {
    if (this.hasWarningMessage()) {
        console.log(this.warningMessage.join(" ").trim());
    }
    if (this._has_errorMessage()) {
        console.error(this.errorMessage.join(" ").trim());
    } else {
        console.log("Successful");
    }
}

validatesBoundariedSinglePairedCoords(e, n) {
    const e_is_well_boundaried = e >= this.crs1._min_west && e < this.crs1._max_east;
    const n_is_well_boundaried = n >= this.crs1._min_south && n < this.crs1._max_north;
    return e_is_well_boundaried && n_is_well_boundaried;
}

// Define abstract method (if needed)
validatesCoordTypes(crs1, crs2) {
    return this.areCrsMagnasirgasCRSSubclasses(crs1, crs2);
}

areCrsMagnasirgasCRSSubclasses(self, ...many_crs) {
    for (const crs of many_crs) {
        if (!this.isMagnaSirgasCRSSubclass(crs)) {
            return false;
        }
    }
    return true;
}

isMagnaSirgasCRSSubclass(self, crs) {
    return crs instanceof MagnaSirgasCRS;
}