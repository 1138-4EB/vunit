.. _vc_library:

Verification Component Library
==============================

.. note:: This is the first non-beta version of this library. Compared
  to previous beta versions, VCs are now split into several repositories
  to easen distributed maintenance.

VUnit contains a number of useful :ref:`Verification Components <verification_components>`
(VC) as well as a set of utilities for writing your own verification
components. Verification components allow a better overview in the test
bench by raising the abstraction level of bus transactions. Even if
you do not need the advanced features that Verification Components (VCs)
offer, you may still benefit from using pre-verified models of e.g. an
AXI-bus instead of re-implementing it yourself.

All of the VCs are built on top of :ref:`Verification
Component Interfaces <verification_component_interfaces>` (VCI). A
single VC typically implements several VCIs. For example an AXI-lite
VC or RAM master VC can support the same generic bus master and
synchronization VCI while also supporting their own bus specific VCIs.

.. TIP:: The main benefit of generic VCIs is to reduce redundancy between
   VCs and allow the user to write generic code that will work regardless
   of the specific VC instance used. For example control registers might be
   defined as a RAM-style bus in a submodule but be mapped to an AXI-lite
   interface on the top level. The same testbench code for talking to the
   submodule can be used in both the submodule test bench as well as the
   top level test bench regardless of the fact that two different VCs
   have been used. Without generic VCIs copy pasting the code and
   changing the type of read/write procedure call would be required.

Neither a VC or a VCI there is the :ref:`memory model <memory_model>`
which is a model of a memory space such as the DRAM address space in a
computer system. The memory mapped slave VCs such as AXI and Wishbone
make transactions against the memory model which provides access
permissions, expected data settings as well as the actual buffer for
reading and writing data.

.. toctree::
   :maxdepth: 1
   :hidden:

   memory_model

.. _verification_component_interfaces:

Verification Component Interfaces
---------------------------------

A verification component interface (VCI) is a procedural interface to
a VC. A VCI is defined as procedures in a package file. Several VCs can
support the same generic VCI to enable code re-use both for the users
and the VC-developers.

List of VCIs included in the main repository:

Included verification component interfaces (VCIs):

* :ref:`Bus master <bus_master_vci>`: generic read and write of bus with address and byte enable.
* :ref:`Stream <stream_vci>`: push and pop of data stream without address.
* :ref:`Synchronization <sync_vci>`: wait for time and events.

.. toctree::
   :maxdepth: 1
   :hidden:

   vci

.. _verification_components:

Verification Components
-----------------------

A verification component (VC) is an entity that is normally connected
to the Design Under Test (DUT) via a bus signal interface such as AXI-Lite.
The main test sequence in the test bench sends messages to the VCs that
will then perform the actual bus signal transactions. The benefit of
this is both to raise the abstraction level of the test bench as well as
making it easy to have parallel activity on several bus interfaces.

A VC typically has an associated package defining procedures for
sending to and receiving messages from the VC. Each VC instance is
associated with a handle that is created in the test bench and set as
a generic on the VC instantiation. The handle is given as and argument
to the procedure calls to direct messages to the specfic VC instance.

Except for `RAM master <BROKEN_LINK>`_, the VCs are neither included in
the main VUnit repository nor provided in the :ref:`PyPi package <installing_pypi>`.
However, the :ref:`cli` provides a ``Warehouse`` class with methods to
automate the addition of third-party VC sources.

List of known VCs:

- Avalon:

  - Memory-Mapped master
  - Memory-Mapped slave
  - Streaming sink
  - Streaming source
- Wishbone

  - Master
  - Slave
