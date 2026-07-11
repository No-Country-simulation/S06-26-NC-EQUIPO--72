package com.example.appbitb2g.enums;

public enum ClusterValue {
	A("A"),
	B("B"),
	C("C"),
	D("D");

	private final String value;

	ClusterValue(String value) {
		this.value = value;
	}

	public static ClusterValue fromString(String text) {
		if (text == null) return null;
		for (ClusterValue b : ClusterValue.values()) {
			if (b.value.equalsIgnoreCase(text)) {
				return b;
			}
		}
		return null;
	}
}
