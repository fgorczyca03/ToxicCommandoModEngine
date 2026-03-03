# File Format Research Notes

## Goal

Document container structure and metadata fields for packed game files.

## Initial assumptions

- The game likely stores assets in one or more container formats (e.g., `.pak`, `.pck`, `.bin`, `.dat`).
- Containers may include a central index/table with offsets, sizes, and asset identifiers.
- Script metadata extraction should prefer immutable read-only parsing.

## Research checklist

- [ ] Identify magic bytes/signatures for each container type.
- [ ] Locate index/table boundaries.
- [ ] Map fields: path/name hash, offset, compressed size, uncompressed size, flags/type.
- [ ] Determine compression/encryption flags.
- [ ] Verify if separate `.idx` / `.toc` files reference payload containers.

## Safety policy

- Do not commit extracted payload files.
- Do not include copyrighted game content in this repository.
- Commit only scripts, metadata schemas, and format notes.
