from blockdiag_fences import main as fencesMain


def main():
    image = fencesMain.fence_img_format(
        """
        blockdiag {
            // Set labels to nodes.
            A [label = "foo"];
            B [label = "bar"];
            // And set text-color
            C [label = "baz"];
            // Set labels to edges. (short text only)
            A -> B [label = "click bar", textcolor="red"];
            B -> C [label = "click baz"];
            C -> A;
        }
        """,
        "blockdiag"
    )
    print(image)


if __name__ == "__main__":
    main()
