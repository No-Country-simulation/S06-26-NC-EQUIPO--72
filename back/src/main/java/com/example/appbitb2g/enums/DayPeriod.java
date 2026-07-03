package com.example.appbitb2g.enums;

import lombok.Getter;

@Getter
public enum DayPeriod {
	MADRUGADA("MADRUGADA"),
	MANHA("MANHA"),
	TARDE("TARDE"),
	NOITE("NOITE");

	private final String value;

	DayPeriod(String value) {
		this.value = value;
	}

	public static DayPeriod fromString(String text) {
		if (text == null) return null;
		for (DayPeriod b : DayPeriod.values()) {
			if (b.value.equalsIgnoreCase(text)) {
				return b;
			}
		}
		return null;
	}
}
